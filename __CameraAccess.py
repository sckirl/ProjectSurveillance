# CameraAccess.py

import cv2
from ultralytics import YOLO
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QImage, QPixmap
import pytesseract
import re
import numpy as np
import time

class CameraWorker(QObject):
    # Signals remain the same
    frameUpdated = Signal(QPixmap)
    visionStatus = Signal(str)
    detectionOccurred = Signal(bytes, str, str, str)
    finished = Signal()

    def __init__(self, model_path, camera_index):
        super().__init__()
        self.model = YOLO(model_path)
        self.camera_index = camera_index
        self.is_running = False
        self.seen_ids = set()
        
        self.detection_buffer = []
        self.last_process_time = time.time()
        self.processing_interval = 0.5
        
        self.last_detection_time = 0  # Timestamp of the last valid detection event
        
        self.roi_latitude = (20, 400, 200, 40)
        self.roi_longitude = (420, 400, 200, 40)

    def _perform_ocr(self, frame, roi):
        x, y, w, h = roi
        roi_img = frame[y:y+h, x:x+w]
        hsv = cv2.cvtColor(roi_img, cv2.COLOR_BGR2HSV)
        lower_white = np.array([0, 0, 180])
        upper_white = np.array([255, 50, 255])
        mask = cv2.inRange(hsv, lower_white, upper_white)
        config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789.-'
        text = pytesseract.image_to_string(mask, config=config)
        cleaned_text = re.sub(r'[^\d.-]', '', text).strip()
        return cleaned_text if cleaned_text else "N/A"

    def process_detection_buffer(self):
        if not self.detection_buffer:
            return

        best_frame_data = None
        max_new_ids_count = 0

        for frame_data in self.detection_buffer:
            new_ids = frame_data['track_ids'] - self.seen_ids
            if len(new_ids) > max_new_ids_count:
                max_new_ids_count = len(new_ids)
                best_frame_data = frame_data

        # Check if we found a frame with at least one new ID
        if best_frame_data and max_new_ids_count > 0:
            current_time = time.time()
                
            # --- If all conditions met, proceed ---
            lat_text = self._perform_ocr(best_frame_data['original_frame'], self.roi_latitude)
            lon_text = self._perform_ocr(best_frame_data['original_frame'], self.roi_longitude)

            success, buffer = cv2.imencode('.jpg', best_frame_data['annotated_frame'])
            if success:
                image_bytes = buffer.tobytes()
                newly_detected_ids = best_frame_data['track_ids'] - self.seen_ids
                detection_message = f"Detected {len(newly_detected_ids)} new object(s). IDs: {list(newly_detected_ids)}"
                
                # 1. Emit the signal to the main GUI
                self.detectionOccurred.emit(image_bytes, detection_message, lat_text, lon_text)
                
                # 2. Update the master list of seen IDs
                self.seen_ids.update(best_frame_data['track_ids'])

                # 3. Reset the cooldown timer
                self.last_detection_time = current_time
        
        # Clear the buffer regardless, to start fresh for the next interval
        self.detection_buffer.clear()

    @Slot()
    def run(self):
        self.is_running = True
        self.camera = cv2.VideoCapture(self.camera_index)
        self.visionStatus.emit("Camera feed starting...")
        
        while self.is_running:
            success, frame = self.camera.read()
            if not success: continue

            results = self.model.track(source=frame, persist=True, verbose=False, tracker='botsort.yaml', conf=0.4)
            annotated_frame = cv2.resize(results[0].plot(), (640, 480))

            lx, ly, lw, lh = self.roi_latitude
            cv2.rectangle(annotated_frame, (lx, ly), (lx + lw, ly + lh), (0, 0, 255), 2)
            lonx, lony, lonw, lonh = self.roi_longitude
            cv2.rectangle(annotated_frame, (lonx, lony), (lonx + lonw, lony + lonh), (0, 0, 255), 2)
            
            if results[0].boxes.id is not None:
                track_ids = set(results[0].boxes.id.cpu().numpy().astype(int))
                self.detection_buffer.append({
                    'original_frame': frame.copy(),
                    'annotated_frame': annotated_frame,
                    'track_ids': track_ids
                })

            current_time = time.time()
            if current_time - self.last_process_time > self.processing_interval:
                self.process_detection_buffer()
                self.last_process_time = current_time

            rgb_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            qt_pixmap = QPixmap.fromImage(qt_image)
            self.frameUpdated.emit(qt_pixmap)

    def stop(self):
        self.is_running = False