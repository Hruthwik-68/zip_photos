from django.db import models

class PhotoUpload(models.Model):
    zip_file = models.FileField(upload_to='uploads/')
