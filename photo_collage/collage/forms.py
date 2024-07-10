# collage/forms.py
from django import forms
from .models import PhotoUpload

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = PhotoUpload
        fields = ['zip_file']
