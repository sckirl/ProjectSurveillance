import serial
import time
import struct
from PySide6.QtCore import QObject, Signal, Slot

# Drone Communication, on separate Thread
class Drone:
    """Handles the low-level MSP communication."""
    def __init__(self, com_port, baud_rate=115200):
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.ser = None
        self.MSP_RAW_IMU = 102

    def connect(self):
        try:
            self.ser = serial.Serial(self.com_port, self.baud_rate, timeout=1)
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

    def read_imu_data(self):
        if not self.ser or not self.ser.is_open:
            return None
            
        try:
            request_packet = self.construct_msp_request(self.MSP_RAW_IMU)
            self.ser.write(request_packet)
            time.sleep(0.05)
            response_data = self.ser.read_all()

            if response_data.startswith(b'$M>') and len(response_data) >= 23:
                payload = response_data[5:23]
                sensors = struct.unpack('<9h', payload)
                return sensors[3:6] # Return (gyro_x, gyro_y, gyro_z)
        except (serial.SerialException, struct.error):
            return None
        return None


class DroneWorker(QObject):
    # Signal to send data back to the main UI thread
    gyro_data_updated = Signal(tuple)
    connection_status = Signal(str)

    def __init__(self, com_port):
        super().__init__()
        self.drone = Drone(com_port)
        self.is_running = False

    @Slot()
    def run(self):
        """This method will run in the background thread."""
        self.is_running = True
        
        if not self.drone.connect():
            self.connection_status.emit(f"Failed to connect to {self.drone.com_port}")
            self.is_running = False
            return
            
        self.connection_status.emit(f"Connected to {self.drone.com_port}")

        while self.is_running:
            gyro_data = self.drone.read_imu_data()
            if gyro_data:
                self.gyro_data_updated.emit(gyro_data)
            time.sleep(0.05) # Control the loop speed

        self.drone.disconnect()
        self.connection_status.emit("Disconnected")

    def stop(self):
        self.is_running = False