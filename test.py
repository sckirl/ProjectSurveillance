import serial
import time

# --- Configuration ---
# Replace with your serial port name
# On Windows: 'COM3', 'COM4', etc.
# On macOS/Linux: '/dev/tty.usbserial-XXXX', '/dev/ttyUSB0', etc.
SERIAL_PORT = '/dev/tty.usbserial-0001'  

# CRSF protocol uses a baud rate of 420000
BAUD_RATE = 9200

try:
    # Initialize the serial connection
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Successfully connected to {SERIAL_PORT} at {BAUD_RATE} baud.")

    while True:
        # Read a chunk of data from the serial port
        # The data comes in as raw bytes
        data_bytes = ser.read(128) # Read up to 128 bytes

        if data_bytes:
            print(f"Received {len(data_bytes)} bytes: {data_bytes.hex(':')}")

        time.sleep(0.1) # Don't spam the CPU

except serial.SerialException as e:
    print(f"Error: Could not open serial port {SERIAL_PORT}. Details: {e}")
except KeyboardInterrupt:
    print("\nProgram stopped by user.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")