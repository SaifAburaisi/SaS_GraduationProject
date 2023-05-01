import io
from PIL import Image as im
import torch
import base64
from django.shortcuts import render
from django.views.generic.edit import CreateView

from .models import ImageModel
from .Forms import ImageUploadForm



class UploadImage(CreateView):
    model = ImageModel
    template_name = 'upload.html'
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

            results = model(img, size=608)
            results.render()
            for img in results.imgs:
                img_base64 = im.fromarray(img)
                img_base64.save("C:\\Users\\User\\Desktop\\stady\\Grad. Project\\SaS_GraduationProject\\SaS_Web_Application\\model\\templates\\image0.jpg", format="JPEG")
            image = open("C:\\Users\\User\\Desktop\\stady\\Grad. Project\\SaS_GraduationProject\\SaS_Web_Application\\model\\templates\\image0.jpg", "rb").read()
            inference_img = base64.b64encode(image).decode()

            form = ImageUploadForm()
            context = {
                "form": form,
                "inference_img": inference_img
            }
            return render(request, 'upload.html', context)

        else:
            form = ImageUploadForm()
        context = {
            "form": form
        }
        return render(request, 'upload.html', context)