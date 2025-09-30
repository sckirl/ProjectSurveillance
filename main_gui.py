from PySide6.QtWidgets import *
from PySide6.QtMultimedia import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QFile
from PySide6.QtWebEngineWidgets import QWebEngineView

# QT Threading things
from PySide6.QtCore import QFile, QThread, Slot, Qt
from PySide6.QtGui import QPixmap

import folium
import io
import sys
from serial.tools import list_ports

# Internal classes
from CameraAccess import CameraWorker
from DatabaseAccess import DatabaseWorker

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

        # ------ Internal Classes Initialization -------
        self.database = DatabaseWorker(server="localhost",
                                       port=1433, 
                                       user="sa",
                                       password="N0t3431@lv",
                                       database="master")
        

        # Start threadings babyyy
        self.camera_thread = None
        self.camera_worker = None

        # Attach all the ui things and get all the ports
        self.uiComponents()

        # Get all the coded things
        self.getSerialPorts()
        self.getCameraLabels()
        self.getMap()
        self.serial_combo_box.addItem("")

    def uiComponents(self):
        # Tab 1
        self.serial_combo_box = self.ui.findChild(QComboBox, "SerialComboBox")
        self.camera_combo_box = self.ui.findChild(QComboBox, "CameraComboBox")
        self.read_button = self.ui.findChild(QPushButton, "readButton")
        self.map_view = self.ui.findChild(QWebEngineView, "MapWebView")

        # Tab 2
        self.save_button = self.ui.findChild(QPushButton, "saveDatabase")
        self.latitude_edit = self.ui.findChild(QLineEdit, "latitudeEdit")
        self.longitude_edit = self.ui.findChild(QLineEdit, "longitudeEdit")
        self.altitude_edit = self.ui.findChild(QLineEdit, "altitudeEdit")

        # Camera Setup
        self.video_widget = self.ui.findChild(QLabel, "videoDisplayWidget")
        
        # New: Add a QLabel in your .ui file with the name "captureDisplayWidget"
        self.capture_display = self.ui.findChild(QLabel, "captureDisplayWidget")

        if self.read_button:
            self.read_button.clicked.connect(self.startCameraConnection)
        
    def getSerialPorts(self):
        if self.serial_combo_box:
            self.serial_combo_box.clear() # Clear existing items
            ports = list_ports.comports()
            for port in ports:
                self.serial_combo_box.addItem(port.device)

    def getCameraLabels(self):
        if self.camera_combo_box:
            self.camera_combo_box.clear() 
            self.camera_devices = QMediaDevices.videoInputs()

            if not self.camera_devices:
                print("No camera devices found")
                return
            
            for camera in self.camera_devices:
                self.camera_combo_box.addItem(camera.description()) 

    def getMap(self):
        # Get the map data from folium
        jakarta_coords = [-6.2088, 106.8456]
        m = folium.Map(location=jakarta_coords, zoom_start=15)

        # Add a marker for Monas
        folium.Marker(
            location=[-6.1754, 106.8272],
            popup="Monas",
            tooltip="Click Here!"
        ).add_to(m)

        # Save map data to an in-memory buffer
        data = io.BytesIO()
        m.save(data, close_file=False)

        
        if self.map_view:
            # Set the HTML from the in-memory buffer
            self.map_view.setHtml(data.getvalue().decode())

    def startCameraConnection(self):
        # Stop any existing worker before starting a new one
        if self.camera_thread and self.camera_thread.isRunning():
            self.camera_worker.stop()
            self.camera_thread.quit()
            self.camera_thread.wait()

        # 1. Create a QThread
        self.camera_thread = QThread()
        
        # 2. Create an instance of your CameraWorker
        selected_camera_index = self.camera_combo_box.currentIndex()
        self.camera_worker = CameraWorker(model_path="MODELS/HumanDetect.pt", 
                                          camera_index=selected_camera_index)
                                          
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

    def sendDatabaseData(self):

        if self.toSend:
            latitude = str(self.latitude_edit.text())
            altitude = str(self.altitude_edit.text())
            longitude = str(self.longitude_edit.text())

            # This now saves data without an image (manual trigger)
            self.database.insertCoordinates(latitude=latitude, 
                                            longitude=longitude, 
                                            altitude=altitude,
                                            img=self.image_data)
            
            print("SUCCESSFULLY INSERTED Manually")
            self.toSend = False

    # This slot receives the QPixmap from the worker thread
    @Slot(QPixmap)
    def updateCameraFeed(self, pixmap):
        self.video_widget.setPixmap(pixmap)
        
    # New: This slot handles the detection signal
    @Slot(bytes, str)
    def handleDetection(self, image_data, message):
        """Saves detection data to DB and updates UI."""
        # print(f"Notification: {message}")

        if self.save_button:
            # TODO: optimize this thing lmao
            self.image_data = image_data
            # This button is now for manual saves, but only appears when detection happens
            self.save_button.clicked.connect(self.sendDatabaseData)
            self.toSend = True
        
        # Show the captured image in the UI
        if self.capture_display:
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            # Scale it to fit the label while keeping aspect ratio
            self.capture_display.setPixmap(pixmap.scaled(
                self.capture_display.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))


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