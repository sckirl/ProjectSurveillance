from PySide6.QtWidgets import *
from PySide6.QtMultimedia import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QFile
from PySide6.QtWebEngineWidgets import QWebEngineView

# QT Threading things
from PySide6.QtCore import QFile, QThread, Slot
from PySide6.QtGui import QPixmap

import folium
import io
import sys
from serial.tools import list_ports

# Internal classes
from DroneAccess import DroneWorker
from CameraAccess import CameraWorker

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        ui_file = QFile("MainInterface/form.ui")
        ui_file.open(QFile.ReadOnly)
        self.camera = CameraWorker(model_path="MODELS/HumanDetect.pt",
                                                camera_index=0)
        self.ui = loader.load(ui_file, self)   # load UI
        ui_file.close()

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
        self.serial_combo_box = self.ui.findChild(QComboBox, "SerialComboBox")
        self.camera_combo_box = self.ui.findChild(QComboBox, "CameraComboBox")
        self.read_button = self.ui.findChild(QPushButton, "readButton")
        self.map_view = self.ui.findChild(QWebEngineView, "MapWebView")
        self.gyro_data_label = self.ui.findChild(QLabel, "gyroDataLabel")
        
        # Camera Setup
        self.video_widget = self.ui.findChild(QLabel, "videoDisplayWidget")
        
        if self.read_button:
            self.read_button.clicked.connect(self.startCameraConnection)

    def startThreads(self):
        self.drone_thread = None
        self.drone_worker = None

        self.camera_thread = None
        self.camera_worker = None

    def getSerialPorts(self):
        if self.serial_combo_box:
            self.serial_combo_box.clear() # Clear existing items
            ports = list_ports.comports()
            for port in ports:
                self.serial_combo_box.addItem(port.device)

    def getCameraLabels(self):
        if self.camera_combo_box:
            self.camera_combo_box.clear() # Clear existing items
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
        
        # Connect the frameUpdated signal to a slot in the UI
        self.camera_worker.frameUpdated.connect(self.update_camera_feed)

        # 5. Start the thread
        self.camera_thread.start()
        print(f"Starting camera feed on thread: {self.camera_thread.currentThread()}")

        self.startDroneConnection()

    def startDroneConnection(self):
        selected_com_port = self.serial_combo_box.currentText()
        if not selected_com_port:
            print("No COM port selected for drone.")
            return

        self.drone_thread = QThread()
        self.drone_worker = DroneWorker(com_port=selected_com_port)
        self.drone_worker.moveToThread(self.drone_thread)
        
        # Connect signals
        self.drone_thread.started.connect(self.drone_worker.run)
        self.drone_worker.finished.connect(self.drone_thread.quit)
        # --- MODIFIED: Connect the signal to the new slot ---
        self.drone_worker.gyro_data_updated.connect(self.update_gyro_display)
        self.drone_worker.connection_status.connect(lambda status: print(f"Drone Status: {status}"))
        
        self.drone_thread.start()
        self.read_button.setText("Stop Connection")

    # This slot receives the QPixmap from the worker thread
    @Slot(QPixmap)
    def update_camera_feed(self, pixmap):
        """Updates the video_widget with a new pixmap."""
        self.video_widget.setPixmap(pixmap)

    @Slot(tuple)
    def update_gyro_display(self, gyro_data):
        # --- NEW/MODIFIED: This slot now updates the text label ---
        # Format the tuple into a readable string
        gyro_text = f"Gyro (X, Y, Z):  {gyro_data[0]}, {gyro_data[1]}, {gyro_data[2]}"
        
        # Set the text on the label
        if self.gyro_data_label:
            self.gyro_data_label.setText(gyro_text)

    # Cleanly stop the thread when the window is closed
    def closeEvent(self, event):
        print("Closing window...")
        if self.camera_thread and self.camera_thread.isRunning():
            self.camera_worker.stop()
            self.camera_thread.quit()
            self.camera_thread.wait()
        event.accept()

        if self.drone_thread and self.drone_thread.isRunning():
            self.drone_worker.stop()
            self.drone_thread.quit()
            self.drone_thread.wait()
            print("Drone thread stopped.")

        self.read_button.setText("Start Connection")


if __name__ == "__main__":
    app = QApplication([])
    window = MainUI()
    window.ui.show()
    sys.exit(app.exec())