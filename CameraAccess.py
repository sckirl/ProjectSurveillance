import cv2
from ultralytics import YOLO
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QImage, QPixmap
import time 

import pytesseract
import re

class CameraWorker(QObject):
    # Signals to send data back to the main UI thread
    frameUpdated = Signal(QPixmap)
    visionStatus = Signal(str)
    detectionOccurred = Signal(bytes, str)
    finished = Signal()

    detectionOccurred = Signal(bytes, str, str, str) # image_bytes, message, latitude, longitude
    finished = Signal()

    def __init__(self, model_path, camera_index):
        super().__init__()
        self.model = YOLO(model_path)
        self.camera_index = camera_index
        self.is_running = False
        self.seen_ids = set()

        self.roi_latitude = (25, 50, 200, 40)
        self.roi_longitude = (25, 90, 200, 40)

    def _perform_ocr(self, frame, roi):
        """Crops the frame to the ROI, preprocesses, and runs OCR."""
        x, y, w, h = roi
        
        # Crop the image to the defined ROI
        roi_img = frame[y:y+h, x:x+w]
        
        # Pre-process for better OCR results: grayscale and thresholding
        gray = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Use pytesseract to extract text
        # Config helps to treat the image as a single line of text with numbers
        config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789.-'
        text = pytesseract.image_to_string(thresh, config=config)
        
        # Clean up the text: remove newlines and other unwanted characters
        cleaned_text = re.sub(r'[^\d.-]', '', text).strip()
        
        return cleaned_text if cleaned_text else "N/A"
    
    @Slot()
    def run(self):
        self.is_running = True
        self.camera = cv2.VideoCapture(self.camera_index)
        self.visionStatus.emit("Camera feed starting...")
        
        while self.is_running:
            success, frame = self.camera.read()

            # Use model.track for a continuous stream of results with persistent tracking
            results = self.model.track(source=frame, 
                                                persist=True, 
                                                verbose=False,
                                                tracker='botsort.yaml',
                                                conf=0.6)
            
            # Start with the original frame for annotations
            annotated_frame = cv2.resize(results[0].plot(), (640, 480))
            
            # --- 1. Robustness: Check if tracking IDs exist before processing ---
            # This `if` statement is the key to preventing crashes on empty frames.
            if results[0].boxes.id is not None:
                # --- 2. Draw the actual annotator to the screen ---
                # The plot() method draws all boxes, labels, and IDs.
                track_ids = results[0].boxes.id.cpu().numpy().astype(int)

                # ================= Cek object apakah sudah pernah terdeteksi
                is_new = False
                for track_id in track_ids:
                    # Check if this is a new ID
                    if track_id not in self.seen_ids:
                        is_new = True
                        self.seen_ids.add(track_id)
                
                # ================== Kirim alert saat ada object terdeteksi berapapun
                if is_new:
                    detection_message = f"New object detected! ID"
                    
                    lat_text = self._perform_ocr(frame, self.roi_latitude)
                    lon_text = self._perform_ocr(frame, self.roi_longitude)
                    
                    # Encode the annotated frame for the signal
                    success, buffer = cv2.imencode('.jpg', annotated_frame)
                    if success:
                        image_bytes = buffer.tobytes()
                        self.detectionOccurred.emit(image_bytes, detection_message, lat_text, lon_text)


                    is_new = False
            # --- Convert Frame for Qt ---
            rgb_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            qt_pixmap = QPixmap.fromImage(qt_image)
        
            self.frameUpdated.emit(qt_pixmap)

    def stop(self):
        """Signals the worker to stop running."""
        self.is_running = False
