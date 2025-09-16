import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QThread, Slot

# Import the worker class from our logic file
from DroneAccess import DroneWorker
# Import the generated UI class
from InterfaceAccess import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set up the user interface from the generated file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Threading setup remains the same
        self.thread = None
        self.worker = None

        # Connect button click event to our logic
        # Note that we now access the button via `self.ui.connect_button`
        self.ui.connect_button.clicked.connect(self.toggle_connection)

    def toggle_connection(self):
        if self.thread is None or not self.thread.isRunning():
            self.ui.connect_button.setText("Disconnect")
            
            # --- This is the core threading logic ---
            self.thread = QThread()
            self.worker = DroneWorker(COM_PORT='/dev/tty.usbmodem0x80000001') # Use your drone's COM port
            
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
            if self.worker:
                self.worker.stop()
            self.ui.connect_button.setText("Connect to Drone")

    # This is a SLOT that receives data from the worker thread
    @Slot(tuple)
    def update_gyro_label(self, gyro_data):
        gx, gy, gz = gyro_data
        # Access the label via `self.ui.gyro_label`
        self.ui.gyro_label.setText(f"Gyro: (x={gx}, y={gy}, z={gz})")
        
    @Slot(str)
    def update_status_label(self, status):
        # Access the label via `self.ui.status_label`
        self.ui.status_label.setText(f"Status: {status}")

# --- Application Entry Point ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())