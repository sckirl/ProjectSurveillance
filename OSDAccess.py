import cv2
import numpy as np
import os
import pytesseract

# --- CONFIGURATION ---
CAMERA_INDEX = "video3.mp4"
FONT_DIR = "osd_font"

# ROI akan disesuaikan secara otomatis berdasarkan ukuran frame
ROIS = {
    "latitude": (110, 120, 110, 23),
    # Tambahkan ROI lain sesuai kebutuhan
}

# --- SETUP TESSERACT ---
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def get_frame_dimensions(cap):
    """Mendapatkan dimensi frame dari video"""
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return width, height

def adjust_roi_to_frame(roi, frame_width, frame_height):
    """Menyesuaikan ROI agar tidak melebihi batas frame"""
    x, y, w, h = roi
    
    # Pastikan koordinat tidak negatif
    x = max(0, x)
    y = max(0, y)
    
    # Pastikan tidak melebihi batas kanan dan bawah
    if x + w > frame_width:
        w = frame_width - x
    if y + h > frame_height:
        h = frame_height - y
    
    # Pastikan width dan height tidak negatif
    w = max(0, w)
    h = max(0, h)
    
    return (x, y, w, h)

def preprocess_for_tesseract(image):
    """Preprocess image untuk meningkatkan akurasi Tesseract"""
    if image.size == 0:
        return image
    
    # Resize image jika terlalu kecil
    if image.shape[0] < 30 or image.shape[1] < 30:
        image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # Apply Gaussian blur untuk mengurangi noise
    blurred = cv2.GaussianBlur(image, (3, 3), 0)
    
    # Thresholding
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return thresh

def ocr_with_tesseract(roi_image):
    """OCR menggunakan Tesseract dengan preprocessing"""
    if roi_image.size == 0:
        return ""
    
    # Preprocess image
    processed_image = preprocess_for_tesseract(roi_image)
    
    # Konfigurasi Tesseract
    config = "--psm 8 -c tessedit_char_whitelist=0123456789.-"
    
    try:
        text = pytesseract.image_to_string(processed_image, config=config)
        return text.strip()
    except Exception as e:
        print(f"Tesseract error: {e}")
        return ""

def load_font_templates(font_directory):
    """Load font templates untuk template matching"""
    templates = {}
    if not os.path.exists(font_directory):
        return None

    for filename in os.listdir(font_directory):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
            
        char_name = filename.split('_')[1].split('.')[0]
        if char_name == 'dot': char_name = '.'
        if char_name == 'dash': char_name = '-'

        template_path = os.path.join(font_directory, filename)
        template_img = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template_img is not None:
            # Threshold template
            _, template_img = cv2.threshold(template_img, 127, 255, cv2.THRESH_BINARY)
            templates[char_name] = template_img

    return templates

def perform_ocr_on_region(roi_image, templates):
    """OCR menggunakan template matching"""
    if not templates or roi_image.size == 0:
        return ""

    # Preprocess ROI
    _, roi_binary = cv2.threshold(roi_image, 127, 255, cv2.THRESH_BINARY)
    
    contours, _ = cv2.findContours(roi_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return ""

    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    sorted_boxes = sorted(bounding_boxes, key=lambda b: b[0])

    detected_string = ""
    for x, y, w, h in sorted_boxes:
        char_image = roi_binary[y:y+h, x:x+w]
        
        if char_image.size == 0:
            continue

        best_match_score = 0.6
        best_match_char = ""

        for char, template in templates.items():
            try:
                # Resize template untuk matching yang lebih baik
                resized_template = cv2.resize(template, (w, h))
                res = cv2.matchTemplate(char_image, resized_template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(res)

                if max_val > best_match_score:
                    best_match_score = max_val
                    best_match_char = char
            except:
                continue

        detected_string += best_match_char

    return detected_string

def debug_roi_display(roi_image, name):
    """Menampilkan ROI untuk debugging"""
    if roi_image.size > 0 and roi_image.shape[0] > 0 and roi_image.shape[1] > 0:
        cv2.imshow(f"ROI {name}", roi_image)

# --- MAIN APPLICATION ---
def main():
    print("Loading font templates...")
    font_templates = load_font_templates(FONT_DIR)
    if not font_templates:
        print(f"Warning: Font directory '{FONT_DIR}' not found or is empty. Using Tesseract only.")

    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print(f"Error: Could not open video file {CAMERA_INDEX}.")
        return

    # Dapatkan dimensi frame
    frame_width, frame_height = get_frame_dimensions(cap)
    print(f"Video dimensions: {frame_width} x {frame_height}")
    
    # Sesuaikan ROI dengan dimensi frame
    adjusted_rois = {}
    for name, roi in ROIS.items():
        adjusted_roi = adjust_roi_to_frame(roi, frame_width, frame_height)
        adjusted_rois[name] = adjusted_roi
        print(f"ROI {name}: Original {roi} -> Adjusted {adjusted_roi}")

    # Jika ROI menjadi terlalu kecil, gunakan ROI default
    for name, (x, y, w, h) in adjusted_rois.items():
        if w < 10 or h < 10:
            print(f"Warning: ROI {name} terlalu kecil, menggunakan ROI default")
            # ROI default di tengah frame
            adjusted_rois[name] = (frame_width//2 - 20, frame_height//2 - 15, 40, 30)

    print("Press 'q' to exit.")
    print("Press 'p' to pause and show debug info.")
    print("Press 'r' to recalibrate ROI positions.")

    paused = False
    
    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                print("End of video or reading error. Restarting...")
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Threshold dengan nilai yang lebih adaptif
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

        output_text = ""
        for name, (x, y, w, h) in adjusted_rois.items():
            # Ambil ROI dari frame
            roi_thresh = thresh[y:y+h, x:x+w]
            
            if roi_thresh.size == 0:
                text = "NO ROI"
                print(f"Warning: Empty ROI for {name}")
            else:
                # Coba template matching terlebih dahulu
                if font_templates:
                    text_manual = perform_ocr_on_region(roi_thresh, font_templates)
                else:
                    text_manual = ""
                
                # Jika template matching gagal, gunakan Tesseract
                if not text_manual or len(text_manual) < 2:
                    text_tesseract = ocr_with_tesseract(roi_thresh)
                    text = text_tesseract if text_tesseract else "NO TEXT"
                else:
                    text = text_manual

            output_text += f"{name.capitalize()}: {text} | "
            
            # Gambar rectangle hijau untuk ROI
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Tambahkan label
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            # Debug display
            if paused:
                debug_roi_display(roi_thresh, name)

        # Tampilkan output text pada frame
        cv2.putText(frame, output_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        print(f"\r{output_text}", end="", flush=True)
        
        cv2.imshow("Drone Video Feed", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('p'):
            paused = not paused
            if paused:
                print("\n--- PAUSED - Press 'p' to continue ---")
            else:
                # Tutup window ROI debug saat melanjutkan
                for name in adjusted_rois.keys():
                    cv2.destroyWindow(f"ROI {name}")
        elif key == ord('r'):
            # Fitur recalibrate - tampilkan dimensi frame
            print(f"\nCurrent frame dimensions: {frame_width} x {frame_height}")
            print("Current ROIs:")
            for name, roi in adjusted_rois.items():
                print(f"  {name}: {roi}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()