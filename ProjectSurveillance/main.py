from CameraAccess import CameraAccess
import WirelessAccess
import time
import cv2
from ultralytics import YOLO
from YOLOdetection import *
from ultralytics.utils.plotting import Annotator, colors
from FrameDifferencing import *
import DroneAccess

# ---- Setup ----
    
NOTIFY_COUNT = 5
LINE_Y = 600

model = YOLO("MODELS/HumanDetect.pt")
drone = DroneAccess.Drone("/dev/tty.usbmodem0x80000001")
object_history = {} 
seenID = set()
sent = True
totalCount = 0
lastCounted = -1 

def main():
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # --- Calculate target dimensions once ---
    ret, firstFrame = cap.read()
    if not ret:
        print("Error: could not read the first frame.")
        cap.release()
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break # End of video

        result = model.predict(frame, conf=0.6, verbose=False)
        annonated = drawAnnotator(frame, result[0])

        """if result[0]:
            drone.readGPS()"""

        # --- Display the Results ---
        cv2.imshow('Detect Human', annonated)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()