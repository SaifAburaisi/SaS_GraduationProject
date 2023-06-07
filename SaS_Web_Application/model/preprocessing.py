import os
import cv2
import numpy as np

def crop_and_resize(img):
    height, width= img.shape[0:2]
    # Crop image
    cropped_img = img[int(height*0.15):int(height*0.85), int(width*0.15):int(width*0.85)]
    # Resize image
    resized_image = cv2.resize(cropped_img, (608, 331))
    return resized_image