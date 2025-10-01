import cv2
import numpy as np
import os
import pytesseract

class OSDReader:
    def __init__(self, tesseract_cmd_path=None, font_dir="osd_font"):
        if tesseract_cmd_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path
        
        # Define the Region of Interest (ROI) for latitude
        # (x, y, width, height) - you may need to adjust these values
        self.roi = (110, 120, 110, 23) 
        
        self.font_templates = self._load_font_templates(font_dir)
        if not self.font_templates:
            print(f"Warning: Font directory '{font_dir}' not found. Using Tesseract only.")

    def _load_font_templates(self, font_directory):
        """Load font templates for template matching."""
        templates = {}
        if not os.path.exists(font_directory):
            return None
        for filename in os.listdir(font_directory):
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
            char_name = os.path.splitext(filename)[0][-1]
            if char_name == 't': char_name = '.'
            if char_name == 'h': char_name = '-'
            template_path = os.path.join(font_directory, filename)
            template_img = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            if template_img is not None:
                _, template_img = cv2.threshold(template_img, 127, 255, cv2.THRESH_BINARY)
                templates[char_name] = template_img
        return templates

    def _preprocess_for_tesseract(self, image):
        """Preprocesses an image to improve Tesseract's accuracy."""
        if image.size == 0: return image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) > 2 else image
        thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]
        return thresh

    def read_latitude_from_image(self, image_bytes):
        """
        Reads the latitude from the OSD of a given image in bytes format.
        """
        try:
            # 1. Decode the image from bytes
            np_arr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if frame is None:
                print("Error: Could not decode image from bytes.")
                return "OCR Error"

            # 2. Extract the Region of Interest (ROI)
            x, y, w, h = self.roi
            
            # Ensure ROI is within frame bounds
            frame_h, frame_w = frame.shape[:2]
            if x + w > frame_w or y + h > frame_h:
                 print("Warning: ROI is outside the frame dimensions.")
                 return "ROI Error"

            roi_frame = frame[y:y+h, x:x+w]

            # 3. Preprocess the ROI for OCR
            processed_roi = self._preprocess_for_tesseract(roi_frame)

            # 4. Perform OCR using Tesseract
            config = "--psm 8 -c tessedit_char_whitelist=0123456789.-"
            text = pytesseract.image_to_string(processed_roi, config=config).strip()

            return text if text else "N/A"

        except Exception as e:
            print(f"An error occurred during OCR processing: {e}")
            return "OCR Exception"
