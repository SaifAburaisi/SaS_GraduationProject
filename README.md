# DenDect
![Alt Text](SaS_Web_Application/model/static/elements/SAS.png)
## Overview
The analysis of dental radiographs is a crucial step in the diagnosis process in routine clinical practice since the dentist must evaluate tooth-related issues throughout the clinical diagnosis. Human error may cause manual analysis to provide false predictions. The automated approach for identifying and categorizing dental issues will help in the early diagnosis of diseases and might help prevent tooth loss. Our goal is to create a model that may offer a second viewpoint and to simplify reporting for dentists. This project suggests a convolutional neural network architecture known as the YOLOv7 that takes panoramic radiographs (X-ray images) as its input and performs multilabel detection of four categories of different teeth problems, that are: conservative (fillings and crowns), implant, RCT (root canal treatment), and bridges.
After undergoing data preprocessing and augmentation, the YOLOv7 architecture is used to detect the teeth problems for its excellent detection quality, its accuracy, and speed. The performance of the model is measured using the mAP metric, our model has achieved a mAP score 90.2%. 

The code in this repositry runs a web application containing a login,home, and upload page. In the upload page you can upload dental panoramic x-ray image, and the model would return the image with the predicted classes for the users viewing.

