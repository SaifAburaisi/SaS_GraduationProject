from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('upload/', views.UploadImage.as_view(), name='upload'),
]