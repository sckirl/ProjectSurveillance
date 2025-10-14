import cv2
from ultralytics import YOLO
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QImage, QPixmap
import pytesseract
import re
import numpy as np
import time

class CameraWorker(QObject):
    frameUpdated = Signal(QPixmap)
    visionStatus = Signal(str)
    detectionOccurred = Signal(bytes, str, str, str)
    finished = Signal()

    def __init__(self, model_path, camera_index, tracker="botsort.yaml", tracks_class=None):
        super().__init__()
        self.model = YOLO(model_path)
        self.camera_index = camera_index
        self.is_running = False
        self.seen_ids = set()
        self.tracker = tracker
        self.tracks_class = tracks_class
        
        # Use a single buffer for clarity. Each item will be a dictionary.
        self.detection_buffer = [] 
        self.last_process_time = time.time()
        self.PROCESS_INTERVAL = 0.5
        
        self.roi_latitude = (20, 390, 200, 30)
        self.roi_longitude = (415, 390, 200, 30)

    def perform_ocr(self, frame, roi):
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
        # 1. Exit early if there's nothing to do
        if not self.detection_buffer:
            return

        # 2. Aggregate all unique object IDs detected during the interval
        all_ids_in_interval = set().union(*(data['ids'] for data in self.detection_buffer))

        # 3. Figure out which of those IDs are actually new
        newly_detected_ids = all_ids_in_interval - self.seen_ids

        # 4. If there are new IDs, create and send one consolidated alert
        if newly_detected_ids:
            # Use the most recent frame's data for the alert image and OCR
            latest_frame_data = self.detection_buffer[-1]
            
            # Perform OCR on the original, clean frame for accuracy
            lat_text = self.perform_ocr(latest_frame_data['original_frame'], self.roi_latitude)
            lon_text = self.perform_ocr(latest_frame_data['original_frame'], self.roi_longitude)

            # Prepare the annotated image for the alert
            success, buffer = cv2.imencode('.jpg', latest_frame_data['annotated_frame'])
            if success:
                image_bytes = buffer.tobytes()
                detection_message = f"Detected {len(newly_detected_ids)} new object(s). IDs: {list(newly_detected_ids)}"
                
                # Emit a SINGLE signal for all new detections in this interval
                self.detectionOccurred.emit(image_bytes, detection_message, lat_text, lon_text)
                
                # IMPORTANT: Update the master list with all IDs found in this interval
                self.seen_ids.update(all_ids_in_interval)
        
        # 5. Clear the buffer to start fresh for the next interval
        self.detection_buffer.clear()

    @Slot()
    def run(self):
        self.is_running = True
        self.camera = cv2.VideoCapture(self.camera_index)
        self.visionStatus.emit("Camera feed starting...")
        
        while self.is_running:
            success, frame = self.camera.read()
            if not success: continue

            # TODO: get rid of this ugly ahh thing bro HAHA but also this just works, idk
            if self.tracks_class and len(self.tracks_class) > 0:
                results = self.model.track(source=frame, 
                                        persist=True, 
                                        verbose=False, 
                                        tracker=self.tracker, 
                                        conf=0.4, 
                                        classes=self.tracks_class)

            else:
                results = self.model.track(source=frame, 
                                        persist=True, 
                                        verbose=False, 
                                        tracker=self.tracker, 
                                        conf=0.4)
                

            annotated_frame = cv2.resize(results[0].plot(), (640, 480))

            lx, ly, lw, lh = self.roi_latitude
            cv2.rectangle(annotated_frame, (lx, ly), (lx + lw, ly + lh), (0, 0, 255), 2)
            lonx, lony, lonw, lonh = self.roi_longitude
            cv2.rectangle(annotated_frame, (lonx, lony), (lonx + lonw, lony + lonh), (0, 0, 255), 2)
            
            if results[0].boxes.id is not None:
                track_ids = set(results[0].boxes.id.cpu().numpy().astype(int).flatten())
                # Add a dictionary to the buffer containing all necessary data
                self.detection_buffer.append({
                    'original_frame': frame.copy(),
                    'annotated_frame': annotated_frame,
                    'ids': track_ids
                })

            current_time = time.time()
            if current_time - self.last_process_time > self.PROCESS_INTERVAL:
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
        # Add camera release
        if hasattr(self, 'camera') and self.camera.isOpened():
            self.camera.release()