import cv2
import numpy as np
import os

def is_rectangular(contour, min_aspect_ratio=0.3, max_aspect_ratio=5, min_extent=0.85):
    """
    Check if a contour is approximately rectangular.
    min_aspect_ratio: minimum aspect ratio (width/height)
    max_aspect_ratio: maximum aspect ratio (width/height)
    min_extent: minimum extent (contour area / bounding box area)
    """
    x, y, w, h = cv2.boundingRect(contour)
    if w<256 or h<256: #specific requirements for my projects
        return False
    aspect_ratio = w / float(h)
    contour_area = cv2.contourArea(contour)
    bounding_box_area = w * h
    extent = contour_area / bounding_box_area

    return min_aspect_ratio <= aspect_ratio <= max_aspect_ratio and extent >= min_extent


def extract_panels_from_image(image_path):
    panel_number = 1
    # image_path = 'data/vol1/Invincible, Vol. 1_0012.jpg'

    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[1])
    min_contour_area = 256*256
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area and is_rectangular(cnt)]
    filtered_contours = sorted(filtered_contours, key=lambda ctr: cv2.boundingRect(ctr)[1])

    
    for contour in filtered_contours:
        x, y, w, h = cv2.boundingRect(contour)
        panel = image[y:y+h, x:x+w]
        panel_path = f'scenery/ExMachina/'+os.path.basename(image_path)+'panel_'+str(panel_number)+'.jpg'
        cv2.imwrite(panel_path, panel)
        panel_number += 1

def process_folder(folder_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    image_files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in image_extensions]

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        extract_panels_from_image(image_path)

process_folder('Panels/ExMachina')