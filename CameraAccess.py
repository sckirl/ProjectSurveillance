import cv2
from ultralytics import YOLO
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QImage, QPixmap

class CameraWorker(QObject):
    # Signals to send data back to the main UI thread
    frameUpdated = Signal(QPixmap)
    visionStatus = Signal(str)
    detectionOccurred = Signal(bytes, str)
    finished = Signal()

    def __init__(self, model_path, camera_index):
        super().__init__()
        self.model = YOLO(model_path)
        self.camera_index = camera_index
        self.is_running = False
        self.seen_ids = set()

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
                                                conf=0.7)
            
            # Start with the original frame for annotations
            annotated_frame = cv2.resize(results[0].plot(), (640, 480))
            
            # --- 1. Robustness: Check if tracking IDs exist before processing ---
            # This `if` statement is the key to preventing crashes on empty frames.
            if results[0].boxes.id is not None:
                # --- 2. Draw the actual annotator to the screen ---
                # The plot() method draws all boxes, labels, and IDs.
                track_ids = results[0].boxes.id.cpu().numpy().astype(int)

                for track_id in track_ids:
                    # Check if this is a new ID
                    if track_id not in self.seen_ids:
                        self.seen_ids.add(track_id)
                        detection_message = f"New object detected! ID: {track_id}"
                        
                        # Encode the annotated frame for the signal
                        success, buffer = cv2.imencode('.jpg', annotated_frame)
                        if success:
                            image_bytes = buffer.tobytes()
                            self.detectionOccurred.emit(image_bytes, detection_message)

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
