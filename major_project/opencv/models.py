from django.db import models
from PIL import Image
import numpy as np
from io import BytesIO
from django.core.files.base import ContentFile
from .utils import get_filtered_image
#import cv2
# Create your models here.
ACTION_CHOICES=(
    ('NO_FILTER','no filter'),
    ('COLORIZED','colorized'),
    ('GRAY_SCALE','grayscale'),
    ('BLURRED','blurred'),
    ('BINARY','binary'),
    ('INVERT','invert'),
)
class Upload(models.Model):
    image=models.ImageField(upload_to="images")
    action=models.CharField(max_length=50,choices=ACTION_CHOICES)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def save(self,*args,**kwargs):
        
        img=Image.open(self.image)
        
        img1=get_filtered_image(img,self.action)
        
        
        buffer=BytesIO()
        img.save(buffer,format="png")
        image_png=buffer.getvalue()
        with open("write.txt","a") as file:
            file.write(str(self.image)+str(" "))
        self.image.save(str(self.image),ContentFile(image_png),save=False)
        super().save(*args,**kwargs)
        
        