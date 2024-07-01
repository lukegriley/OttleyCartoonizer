from PIL import Image
import numpy as np
import random
import os


def extract_from_image(image_path,i):
    image = Image.open(image_path)
    width, height = image.size

    size = 800
    square_size = size if width>size and height>size else min(width,height)
    
    left = random.randint(0, width - square_size)
    top = random.randint(0, height - square_size)
    
    right = left + square_size
    bottom = top + square_size
    box = (left, top, right, bottom)
    
    cropped_image = image.crop(box)
    cropped_image = cropped_image.resize((256,256))

    cropped_image.save(f'scenery/ExMachina/'+str(i)+'.jpg')

def process_folder(folder_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    image_files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in image_extensions]
    count = 0
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        extract_from_image(image_path,count)
        count+=1

# extract_from_image("outputs/Invincible, Vol. 1_0006.jpgpanel_4.jpg")
process_folder('Panels/ExMachina')