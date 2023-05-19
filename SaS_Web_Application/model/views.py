import io
from PIL import Image as im
import torch
import base64
from django.shortcuts import render
from django.views.generic.edit import CreateView

from .models import ImageModel
from .Forms import ImageUploadForm

import cv2
import numpy as np
import random
def get_colors(num_classes):
    random.seed(0)

    # Generate the same colors for each class
    colors = []
    for i in range(num_classes):
        colors.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    return colors

def draw_bounding_boxes(image, results):
    classes = results.names if hasattr(results, 'names') else None
    colors = get_colors(len(classes)) if classes else None
    for *xyxy, conf, cls in results.xyxy[0]:  # for each detection
        label = classes[int(cls)] if classes else str(int(cls))
        color = colors[int(cls)] if colors else (0, 0, 255)  # red color if no colors

        image = cv2.rectangle(image, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), color, 1)

        image = cv2.putText(image, label, (int(xyxy[0]), int(xyxy[1])-5), cv2.FONT_HERSHEY_TRIPLEX, 0.4, (255, 255, 255), 1)
    return image

def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

class UploadImage(CreateView):
    model = ImageModel
    template_name = 'final_upload.html'
    fields = ["image"]

    def post(self, request, *args, **kwargs):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = request.FILES.get('image')
            img_instance = ImageModel(
                image=img
            )
            img_instance.save()

            uploaded_img_qs = ImageModel.objects.filter().last()
            img_bytes = uploaded_img_qs.image.read()
            img = im.open(io.BytesIO(img_bytes))

            # Change this to the correct path
            path_hubconfig = "C:\\Users\\User\\Desktop\\stady\\Grad. Project\\SaS_GraduationProject\\yolov7"
            path_weightfile = "C:\\Users\\User\\Desktop\\stady\\Grad. Project\\SaS_GraduationProject\\SaS_Web_Application\\model\\bestone.pt"  # or any custom trained model

            model = torch.hub.load(path_hubconfig, 'custom',
                                   path_or_model=path_weightfile, source='local')

            results = model(img, size=640)
            numpy_img = np.array(img)
            numpy_img = draw_bounding_boxes(numpy_img, results)
            img_base64 = im.fromarray(numpy_img)
            img_base64.save("C:\\Users\\User\\Desktop\\stady\\Grad. Project\\SaS_GraduationProject\\SaS_Web_Application\\model\\templates\\image0.jpg", format="JPEG")
            image = open("C:\\Users\\User\\Desktop\\stady\\Grad. Project\\SaS_GraduationProject\\SaS_Web_Application\\model\\templates\\image0.jpg", "rb").read()
            inference_img = base64.b64encode(image).decode()

            form = ImageUploadForm()
            context = {
                "form": form,
                "inference_img": inference_img
            }
            return render(request, 'final_upload.html', context)

        else:
            form = ImageUploadForm()
        context = {
            "form": form
        }
        return render(request, 'final_upload.html', context)