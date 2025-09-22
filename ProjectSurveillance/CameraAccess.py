import cv2
from ultralytics import YOLO
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QImage, QPixmap

class CameraWorker(QObject):
    # Signals to send data back to the main UI thread
    frameUpdated = Signal(QPixmap)
    visionStatus = Signal(str)
    finished = Signal()

    def __init__(self, model_path, camera_index):
        super().__init__()
        self.model = YOLO(model_path)
        self.camera_index = camera_index
        self.is_running = False
        self.camera = None

    @Slot()
    def run(self):
        """This method will run in the background thread."""
        self.is_running = True
        self.camera = cv2.VideoCapture(self.camera_index)

        if not self.camera.isOpened():
            self.visionStatus.emit(f"Error: Could not open camera {self.camera_index}.")
            self.is_running = False
            return
            
        self.visionStatus.emit("Camera feed started.")

        while self.is_running:
            ret, frame = self.camera.read()
            frame = cv2.resize(frame, (640, 480))
            if not ret:
                self.is_running = False
                continue

            # --- YOLO Detection ---
            results = self.model.predict(frame, verbose=False)
            annotated_frame = results[0].plot()

            # --- Convert Frame for Qt ---
            rgb_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            qt_pixmap = QPixmap.fromImage(qt_image)
            
            self.frameUpdated.emit(qt_pixmap)

        self.camera.release()
        self.visionStatus.emit("Camera feed stopped.")
        self.finished.emit()

    def stop(self):
        """Signals the worker to stop running."""
        self.is_running = False
