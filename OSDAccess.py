import cv2
import numpy as np
import os

# --- CONFIGURATION ---
CAMERA_INDEX = "Assets/OSDtest.mov"
FONT_DIR = "osd_font" 

# (x, y, width, height)
ROIS = {
    "latitude": (940, 220, 40, 60),
    # "longitude": (0, 145, 300, 40),
    # "altitude": (0, 180, 300, 40),
}

def load_font_templates(font_directory):
    templates = {}
    if not os.path.exists(font_directory): return None
    
    # from each of the "dataset" that was made before, load all those
    for filename in os.listdir(font_directory):
        char_name = filename.split('_')[1].split('.')[0]
        if char_name == 'dot': char_name = '.'
        if char_name == 'dash': char_name = '-'
        
        template_path = os.path.join(font_directory, filename)
        template_img = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template_img is not None:
            templates[char_name] = template_img
    
    return templates

def perform_ocr_on_region(roi_image, templates):
    if not templates: return "[No Templates]"
    # edged = cv2.Canny(roi_image, 30, 200)
    # thresh = cv2.adaptiveThreshold(roi_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    contours, hierarchy = cv2.findContours(roi_image,
                      cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours: return ""
    
    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    sorted_boxes = sorted(bounding_boxes, key=lambda b: b[0])
    
    detected_string = ""
    for x, y, w, h in sorted_boxes:
        char_image = roi_image[y:y+h, x:x+w]
        
        # This prevents poor matches from being accepted.
        best_match_score = 0.5
        best_match_char = ""
        # --- END OF CHANGE ---

        for char, template in templates.items():
            if char_image.shape[0] < template.shape[0] or char_image.shape[1] < template.shape[1]:
                continue
            
            res = cv2.matchTemplate(char_image, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)
            
            if max_val > best_match_score:
                best_match_score = max_val
                best_match_char = char
        
        detected_string += best_match_char


    withCountour = cv2.drawContours(roi_image.copy(), contours, -1, (0, 255, 0), 2)
    cv2.imshow("countor", roi_image)
    return detected_string

# --- MAIN APPLICATION ---

def main():
    print("Loading font templates...")
    font_templates = load_font_templates(FONT_DIR)
    if not font_templates:
        print(f"Error: Font directory '{FONT_DIR}' not found or is empty.")
        return

    print(f"Attempting to open video file: {CAMERA_INDEX}...")
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print(f"Error: Could not open video file {CAMERA_INDEX}.")
        return

    print("\n--- Reading OSD Data ---")
    print("Press 'q' in the video window to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret: 
            # If the video ends, reset it to loop
            print("\nVideo finished. Looping...")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)

        output_text = ""
        for name, (x, y, w, h) in ROIS.items():
            roi_thresh = thresh[y:y+h, x:x+w]
            text = ""
            if roi_thresh.size > 0:
                text = perform_ocr_on_region(roi_thresh, font_templates)
            output_text += f"{name.capitalize()}: {text} | "
            
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        print(f"\r{output_text}", end="")

        cv2.imshow("Drone Video Feed (Press 'q' to quit)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("\n--- Exiting ---")
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()