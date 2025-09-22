import serial
import time
import struct
from PySide6.QtCore import QObject, Signal, Slot

class DroneWorker(QObject):
    # Signals to send data back to the main UI thread
    connection_status = Signal(str)
    gyro_data_updated = Signal(tuple)
    finished = Signal()

    def __init__(self, com_port):
        super().__init__()
        self.com_port = com_port
        self.is_running = False
        self.ser = None
        self.MSP_RAW_IMU = 102

    def connect(self):
        try:
            self.ser = serial.Serial(self.com_port, 115200, timeout=1)
            return True
        except serial.SerialException:
            return False

    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
    
    def construct_msp_request(self, command):
        header = b'$M<'
        payload_size = 0
        size_byte = struct.pack('<B', payload_size)
        command_byte = struct.pack('<B', command)
        checksum = payload_size ^ command
        checksum_byte = struct.pack('<B', checksum)
        return header + size_byte + command_byte + checksum_byte

    @Slot()
    def run(self):
        """Main work loop that runs on the background thread."""
        self.is_running = True
        if not self.connect():
            self.connection_status.emit(f"Failed to connect to {self.com_port}")
            self.is_running = False
        else:
            self.connection_status.emit(f"Connected to {self.com_port}")

        while self.is_running:
            if self.ser and self.ser.is_open:
                try:
                    request_packet = self.construct_msp_request(self.MSP_RAW_IMU)
                    self.ser.write(request_packet)
                    time.sleep(0.05)
                    response_data = self.ser.read_all()

                    if response_data.startswith(b'$M>') and len(response_data) >= 23:
                        payload = response_data[5:23]
                        sensors = struct.unpack('<9h', payload)
                        gyro_data = sensors[3:6]
                        self.gyro_data_updated.emit(gyro_data)
                except serial.SerialException:
                    self.connection_status.emit("Device disconnected.")
                    self.is_running = False
            time.sleep(0.05)

        self.disconnect()
        self.connection_status.emit("Disconnected")
        self.finished.emit()

    def stop(self):
        """Signals the worker to stop running."""
        self.is_running = False

