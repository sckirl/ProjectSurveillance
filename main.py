from PySide6.QtWidgets import *
from PySide6.QtMultimedia import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QThread, Slot, Qt, QTimer
from PySide6.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtGui import QDesktopServices

import sys
from PySide6.QtGui import QImage
import cv2
import numpy as np

# Internal classes
from CameraAccess import CameraWorker
from DatabaseAccess import DatabaseWorker
from MapAccess import MapWorker

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # ------ Necessary PySide6 things, to load from Designer .ui file ------
        loader = QUiLoader()
        ui_file = QFile("InterfaceAccess/form.ui")
        ui_file.open(QFile.ReadOnly)
        
        self.ui = loader.load(ui_file, self)   # load UI
        ui_file.close()
        self.toSend = True
        self.current_record_id = None


        # ------ Internal Classes Initialization -------
        self.database = DatabaseWorker(server="localhost",
                                       port=1433, 
                                       user="sa",
                                       password="N0t3431@lv",
                                       database="master")
        
        
        self.camera_thread = None
        self.camera_worker = None

        # Attach all the ui things and get all the ports
        self.uiComponents()

        # Get all the coded things
        self.getCameraLabels()
        self.loadDatabaseData() # get database data

    def uiComponents(self):
        # Tab 1
        self.camera_combo_box = self.ui.findChild(QComboBox, "CameraComboBox")
        self.read_button = self.ui.findChild(QPushButton, "readButton")
        self.capture_display = self.ui.findChild(QLabel, "captureDisplayWidget")
        self.video_widget = self.ui.findChild(QLabel, "videoDisplayWidget")

        # Tab 2
        self.table_view = self.ui.findChild(QTableView, "tableView")

        # Tab 3
        self.details_tab = self.ui.findChild(QWidget, "DetailsTab")
        self.map_view = self.ui.findChild(QWebEngineView, "MapWebView")
        self.mapWorker = MapWorker(self.map_view) # Map Setup

        self.latitude_edit = self.ui.findChild(QLineEdit, "latitudeEdit")
        self.longitude_edit = self.ui.findChild(QLineEdit, "longitudeEdit")
        self.altitude_edit = self.ui.findChild(QLineEdit, "altitudeEdit")

        self.update_button = self.ui.findChild(QPushButton, "updateBtn")
        self.delete_button = self.ui.findChild(QPushButton, "deleteBtn")

        self.alertSetup()

        # ----------- TRIGGER WHEN BUTTON IS CLICKED -----------
        if self.read_button:
            self.read_button.clicked.connect(self.startCameraConnection)
        if self.table_view:
            self.table_view.doubleClicked.connect(self.getChosenID)
        if self.update_button:
            self.update_button.clicked.connect(self.updateRecordFromDetails)
        if self.delete_button:
            self.delete_button.clicked.connect(self.deleteRecordFromDetails)

    def alertSetup(self):
        self.alert_widget = QFrame(self.video_widget)
        self.alert_widget
        self.alert_widget.setStyleSheet("""
            QFrame {
                background-color: rgba(60, 60, 60, 220);
                border: 1px solid #555;
                border-radius: 8px;
            }
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                background-color: transparent;
                border: none;
            }
            QPushButton {
                padding: 8px 12px;
                font-size: 14px;
            }
        """)
        
        # Create widgets for the alert
        alert_message = QLabel("Terdeteksi Manusia")
        save_button = QPushButton("OK")
        cancel_button = QPushButton("Hapus")
        
        # Create layouts
        button_layout = QHBoxLayout()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        main_alert_layout = QVBoxLayout(self.alert_widget)
        main_alert_layout.addWidget(alert_message, alignment=Qt.AlignmentFlag.AlignTop)
        main_alert_layout.addStretch(1)
        main_alert_layout.addLayout(button_layout)

        self.alert_widget.hide()

        # Connect button signals to methods
        cancel_button.clicked.connect(self.delete_alert)
        save_button.clicked.connect(self.alert_widget.hide)
    
    def loadDatabaseData(self):
        """Fetches all data from the database and populates the tableView."""
        print("Fetching data for table view...")
        records = self.database.fetch_all_data()
        
        # We don't display the large image column in the main table for performance
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['ID', 
                                         'Timestamp', 
                                         'Latitude', 
                                         'Longitude', 
                                         'Altitude'])
        
        for row in records:
            # row[2] is the surveillanceImg, which we skip
            qt_row = [
                QStandardItem(str(row[0])),  # ID
                QStandardItem(str(row[1])),  # Timestamp
                QStandardItem(str(row[3])),  # Latitude
                QStandardItem(str(row[4])),  # Longitude
                QStandardItem(str(row[5]))   # Altitude
            ]
            model.appendRow(qt_row)
            
        self.table_view.setModel(model)
        self.table_view.resizeColumnsToContents()
        print("Table view updated.")

    @Slot()
    def delete_alert(self):
        """Hides the alert and cancels the pending database save."""
        print("Alert dismissed by user. Ignoring detection.")

        last_id = self.database.get_last_id()
        self.database.delete_by_id(last_id)

        self.loadDatabaseData()

        self.alert_widget.hide()
        # Clear the pending data so it doesn't get saved
        self.pending_detection_data = None

    # This method is renamed and simplified
    def save_detection(self):
        image_data, lat_text, lon_text = self.pending_detection_data

        self.database.insertCoordinates(
            latitude=lat_text,
            longitude=lon_text,
            altitude="N/A",
            img=image_data
        )
        print(f"DATABASE INSERT: Lat='{lat_text}', Lon='{lon_text}'")
        self.loadDatabaseData()

        if self.capture_display:
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            self.capture_display.setPixmap(pixmap.scaled(
                self.capture_display.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        
        # Clear the pending data after it's been saved
        self.pending_detection_data = None

    # Replace your old getChosenID method with this one
    def getChosenID(self):
        """Gets ID from the table, fetches the full record, and displays the image."""
        selected_indexes = self.table_view.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "No Selection", "Please select a row from the table first.")
            return

        selected_row = selected_indexes[0].row()
        id_item = self.table_view.model().item(selected_row, 0)
        
        if not id_item:
            QMessageBox.critical(self, "Error", "Could not retrieve ID from the selected row.")
            return

        # Get the data from current selected ID
        self.current_record_id = id_item.text()
        print(f"Loading details for ID: {self.current_record_id}")

        record = self.database.fetch_record_by_id(self.current_record_id)
        if not record:
            QMessageBox.critical(self, "Database Error", f"Could not find record for ID: {self.current_record_id}")
            return

        _, _, image_data, latitude, longitude, altitude = record

        # --- NEW: Populate the QLineEdit fields ---
        # Use `str(value or '')` to handle None values gracefully
        self.latitude_edit.setText(str(latitude or ''))
        self.longitude_edit.setText(str(longitude or ''))
        self.altitude_edit.setText(str(altitude or ''))

        if latitude != "N/A" and longitude != "N/A":
            self.mapWorker.update_map(latitude, longitude)

        if image_data:
            try:
                np_arr = np.frombuffer(image_data, np.uint8)
                img_cv = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                
                if img_cv is None: raise ValueError("Image data could not be decoded.")
                resized_img = cv2.resize(img_cv, (640, 480))

                rgb_image = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w

                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.capture_display.setPixmap(QPixmap.fromImage(qt_image))
            except Exception as e:
                print(f"Error processing image: {e}")
                self.capture_display.setText("Error: Could not load image.")
        else:
            self.capture_display.setText("No image available for this record.")

        if self.details_tab:
            self.ui.tabWidget.setCurrentWidget(self.details_tab)

    def deleteRecordFromDetails(self):
        if not self.current_record_id:
            QMessageBox.warning(self, "No Record Loaded", "Please double click the table to choose record")
            return
        
        # Delete and refresh
        success = self.database.delete_by_id(self.current_record_id)

        if success:
            QMessageBox.information(self, "Success", f"Deleted id: {self.current_record_id} ")
            self.loadDatabaseData() # Refresh the table view to show the new data
        else:
            QMessageBox.critical(self, "Error", "Failed to delete the record in the database.")

    def updateRecordFromDetails(self):
        """Saves the data from the Details tab back to the database."""
        if not self.current_record_id:
            QMessageBox.warning(self, "No Record Loaded", "Please double click the table to choose record")
            return

        # Get the new values from the QLineEdit widgets
        new_latitude = self.latitude_edit.text()
        new_longitude = self.longitude_edit.text()
        new_altitude = self.altitude_edit.text()

        # Call the update method in your DatabaseWorker
        success = self.database.update_coordinates(
            self.current_record_id,
            new_latitude,
            new_longitude,
            new_altitude
        )

        if success:
            QMessageBox.information(self, "Success", "The record has been updated successfully.")
            self.loadDatabaseData() # Refresh the table view to show the new data
        else:
            QMessageBox.critical(self, "Error", "Failed to update the record in the database.")

    def getCameraLabels(self):
        if self.camera_combo_box:
            self.camera_combo_box.clear() 
            self.camera_devices = QMediaDevices.videoInputs()

            if not self.camera_devices:
                print("No camera devices found")
                return
            
            for camera in self.camera_devices:
                self.camera_combo_box.addItem(camera.description()) 

    def startCameraConnection(self):
        # Stop any existing worker before starting a new one
        if self.camera_thread and self.camera_thread.isRunning():
            print("Stopping previous camera thread...")
            self.camera_worker.stop()
            self.camera_thread.quit()
            self.camera_thread.wait() # Wait for it to finish
            print("Previous thread stopped.")
            
        # 1. Create a QThread
        self.camera_thread = QThread()
        
        # 2. Create an instance of your CameraWorker
        selected_camera_index = self.camera_combo_box.currentIndex()
        self.camera_worker = CameraWorker(model_path="MODELS/HumanThermal100.pt", 
                                          camera_index=selected_camera_index, 
                                          )
                                          
        # 3. Move the worker to the thread
        self.camera_worker.moveToThread(self.camera_thread)

        # 4. Connect signals and slots
        self.camera_thread.started.connect(self.camera_worker.run)
        self.camera_worker.finished.connect(self.camera_thread.quit)
        self.camera_worker.finished.connect(self.camera_worker.deleteLater)
        self.camera_thread.finished.connect(self.camera_thread.deleteLater)
        
        self.camera_worker.frameUpdated.connect(self.updateCameraFeed)
        # New: Connect the detection signal to our new handler
        self.camera_worker.detectionOccurred.connect(self.handleDetection)

        # 5. Start the thread
        self.camera_thread.start()

    def sendDatabaseData(self, image_data, latitude=0, 
                         altitude=0, 
                         longitude=0):
        
        # TODO make the latitude, altitude, longitude to automatically write from drone data
        if self.toSend:
            # Esentially just make the ID and the img for now.
            self.database.insertCoordinates(latitude=latitude, 
                                            longitude=longitude, 
                                            altitude=altitude,
                                            img=image_data)
            
            print("SUCCESSFULLY INSERTED TO DATABASE")
            self.toSend = False

            # Update database data again 
            self.loadDatabaseData()

    # This slot receives the QPixmap from the worker thread
    @Slot(QPixmap)
    def updateCameraFeed(self, pixmap):
        self.video_widget.setPixmap(pixmap)
        
    # New: This slot handles the detection signal
    @Slot(bytes, str, str, str)
    def handleDetection(self, image_data, message, lat_text, lon_text):
        """Shows a dismissible alert for a new detection."""
        self.pending_detection_data = (image_data, lat_text, lon_text)

        # Position and show the alert widget
        video_rect = self.video_widget.geometry()
        alert_size = self.alert_widget.sizeHint() # Use sizeHint for auto-sized widgets
        x = (video_rect.width() - alert_size.width()) // 2
        y = (video_rect.height() - alert_size.height()) // 2
        self.alert_widget.move(x, y)
        self.alert_widget.show()

        

        self.save_detection()

    # Cleanly stop the thread when the window is closed
    def closeEvent(self, event):
        if self.camera_thread and self.camera_thread.isRunning():
            self.camera_worker.stop()
            self.camera_thread.quit()
            self.camera_thread.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication([])
    window = MainUI()
    window.ui.show()
    sys.exit(app.exec())