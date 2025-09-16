import sys
import serial
import time
import struct
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import QThread, QObject, Signal, Slot
from DroneAccess import DroneWorker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drone Control UI")
        self.setGeometry(100, 100, 400, 200)

        # UI Elements
        self.gyro_label = QLabel("Gyro: (x, y, z)")
        self.status_label = QLabel("Status: Disconnected")
        self.connect_button = QPushButton("Connect to Drone")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.connect_button)
        layout.addWidget(self.gyro_label)
        layout.addWidget(self.status_label)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Threading setup
        self.thread = None
        self.worker = None

        # Connect button click event
        self.connect_button.clicked.connect(self.toggle_connection)

    def toggle_connection(self):
        if self.thread is None or not self.thread.isRunning():
            self.connect_button.setText("Disconnect")
            
            # --- This is the core threading logic ---
            self.thread = QThread()
            self.worker = DroneWorker(com_port='/dev/tty.usbmodem0x80000001') # Use your drone's COM port
            
            # Move worker to the thread
            self.worker.moveToThread(self.thread)
            
            # Connect signals and slots
            self.thread.started.connect(self.worker.run)
            self.worker.gyro_data_updated.connect(self.update_gyro_label)
            self.worker.connection_status.connect(self.update_status_label)
            
            # Clean up when finished
            self.worker.connection_status.connect(lambda msg: self.thread.quit() if msg != "Connected" else None)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.connection_status.connect(lambda msg: self.worker.deleteLater() if msg != "Connected" else None)

            # Start the thread
            self.thread.start()
        else:
            self.worker.stop()
            self.connect_button.setText("Connect to Drone")

    # This is a SLOT that receives data from the worker thread
    @Slot(tuple)
    def update_gyro_label(self, gyro_data):
        gx, gy, gz = gyro_data
        self.gyro_label.setText(f"Gyro: (x={gx}, y={gy}, z={gz})")
        
    @Slot(str)
    def update_status_label(self, status):
        self.status_label.setText(f"Status: {status}")

# --- Application Entry Point ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())