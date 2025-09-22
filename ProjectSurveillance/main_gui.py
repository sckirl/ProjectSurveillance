from PySide6.QtWidgets import *
from PySide6.QtMultimedia import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QFile
from serial.tools import list_ports
from PySide6.QtWebEngineWidgets import QWebEngineView
import folium
import io
import sys
import cv2

import CameraAccess
from DroneAccess import DroneWorker

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        ui_file = QFile("MainInterface/form.ui")
        ui_file.open(QFile.ReadOnly)
        self.camera = CameraAccess.CameraWorker(model_path="MODELS/HumanDetect.pt",
                                                camera_index=0)
        self.ui = loader.load(ui_file, self)   # load UI
        ui_file.close()

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
        self.layout = self.ui.findChild(QVBoxLayout, "verticalLayoutCamera")
        
        # Camera Setup
        self.capture_session = QMediaCaptureSession()
        self.video_widget = QVideoWidget()
        self.capture_session.setVideoOutput(self.video_widget)
        
        if self.read_button:
            self.read_button.clicked.connect(self.startConnection)

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

    def startConnection(self):
        selectedValue = self.serial_combo_box.currentText()
        selectedCamera = self.camera_combo_box.currentIndex()

        # self.camera = CameraAccess.CameraWorker(model_path="MODELS/HumanDetect.pt",
                                                #camera_index=selectedCamera)
                                            
        self.camera = QCamera(self.camera_devices[selectedCamera])
        self.capture_session.setCamera(self.camera)

        self.capture_session.setVideoOutput(self.video_widget)
        self.layout.addWidget(self.video_widget)

        self.camera.start()


if __name__ == "__main__":
    app = QApplication([])
    window = MainUI()
    window.ui.show()
    sys.exit(app.exec())