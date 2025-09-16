import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import QThread, Slot
from PySide6.QtGui import QPixmap

# Make sure you have these files in the same folder
from DroneAccess import DroneWorker 
from CameraAccess import ComputerVision

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drone Control UI")
        self.setGeometry(100, 100, 800, 600) # Made window larger for video

        # UI Elements
        self.gyro_label = QLabel("Gyro: (x, y, z)")
        self.status_label = QLabel("Status: Disconnected")
        self.video_label = QLabel("Camera feed will be displayed here.")
        self.video_label.setScaledContents(True)

        self.connect_button = QPushButton("Connect to Drone")
        self.camera_button = QPushButton("Start Camera Feed")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.connect_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.gyro_label)
        layout.addSpacing(20) # Add some space
        layout.addWidget(self.camera_button)
        layout.addWidget(self.video_label)
        layout.setStretch(5, 1) # Allow video label to expand

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Threading setup - initialize all to None
        self.drone_thread = None
        self.drone_worker = None
        self.vision_thread = None
        self.vision_worker = None

        # Connect button clicks to their DEDICATED functions
        self.connect_button.clicked.connect(self.toggle_drone_connection)
        self.camera_button.clicked.connect(self.toggle_camera_feed)

    def toggle_drone_connection(self):
        """This function ONLY handles the drone connection."""
        if self.drone_thread is None or not self.drone_thread.isRunning():
            self.connect_button.setText("Disconnect Drone")
            
            self.drone_thread = QThread()
            self.drone_worker = DroneWorker(com_port='/dev/tty.usbmodem0x80000001')
            self.drone_worker.moveToThread(self.drone_thread)
            
            # Connect ONLY drone signals and slots
            self.drone_thread.started.connect(self.drone_worker.run)
            self.drone_worker.gyro_data_updated.connect(self.update_gyro_label)
            self.drone_worker.connection_status.connect(self.update_status_label)
            
            # Cleanup logic
            self.drone_worker.finished.connect(self.drone_thread.quit)
            self.drone_thread.finished.connect(self.drone_worker.deleteLater)
            self.drone_thread.finished.connect(self.drone_thread.deleteLater)

            self.drone_thread.start()
        else:
            if self.drone_worker:
                self.drone_worker.stop()
            self.connect_button.setText("Connect to Drone")

    def toggle_camera_feed(self):
        """This function ONLY handles the camera feed."""
        if self.vision_thread is None or not self.vision_thread.isRunning():
            self.camera_button.setText("Stop Camera Feed")

            self.vision_thread = QThread()
            # Create the worker right when it's needed
            self.vision_worker = ComputerVision(model_path="MODELS/HumanDetect.pt", camera_index=1) # Use 0 for default webcam
            self.vision_worker.moveToThread(self.vision_thread)

            # Connect ONLY vision signals and slots
            self.vision_thread.started.connect(self.vision_worker.run)
            self.vision_worker.frameUpdated.connect(self.update_camera_label)
            self.vision_worker.visionStatus.connect(self.update_status_label)
            
            # Cleanup logic
            self.vision_worker.finished.connect(self.vision_thread.quit)
            self.vision_thread.finished.connect(self.vision_worker.deleteLater)
            self.vision_thread.finished.connect(self.vision_thread.deleteLater)

            self.vision_thread.start()
        else:
            if self.vision_worker:
                self.vision_worker.stop()
            self.camera_button.setText("Start Camera Feed")

    def closeEvent(self, event):
        """Handles closing the window cleanly."""
        print("Closing application...")
        if self.vision_worker:
            self.vision_worker.stop()
        if self.drone_worker:
            self.drone_worker.stop()
        
        if self.vision_thread and self.vision_thread.isRunning():
            self.vision_thread.wait()
        if self.drone_thread and self.drone_thread.isRunning():
            self.drone_thread.wait()
            
        event.accept()
        
    @Slot(tuple)
    def update_gyro_label(self, gyro_data):
        gx, gy, gz = gyro_data
        self.gyro_label.setText(f"Gyro: (x={gx}, y={gy}, z={gz})")
        
    @Slot(str)
    def update_status_label(self, status):
        self.status_label.setText(f"Status: {status}")

    @Slot(QPixmap)
    def update_camera_label(self, frame_pixmap):
        self.video_label.setPixmap(frame_pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

