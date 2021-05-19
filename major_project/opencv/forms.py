from django import forms
from .models import Upload

class ImageForm(forms.ModelForm):
 class Meta:
  model = Upload
  fields = '__all__'
  labels = {'photo':''}