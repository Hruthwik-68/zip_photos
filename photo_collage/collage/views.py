from django.shortcuts import render
from django.conf import settings
from .forms import PhotoUploadForm
from PIL import Image
import os
import zipfile

def create_collage(images, grid_size):
    width, height = images[0].size
    collage_width = width * grid_size
    collage_height = height * grid_size
    collage = Image.new('RGB', (collage_width, collage_height))

    for i in range(grid_size):
        for j in range(grid_size):
            collage.paste(images[i * grid_size + j], (j * width, i * height))

    return collage

def handle_zip_file(zip_file_path, grid_size):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(settings.MEDIA_ROOT)

    extracted_files = [os.path.join(settings.MEDIA_ROOT, f) for f in zip_ref.namelist()]
    images = [Image.open(file) for file in extracted_files if file.endswith(('jpg', 'jpeg', 'png'))]

    if len(images) != grid_size ** 2:
        raise ValueError(f"Expected {grid_size ** 2} images, but got {len(images)}")

    collage = create_collage(images, grid_size)
    collage_path = os.path.join(settings.MEDIA_ROOT, 'collage.jpg')
    collage.save(collage_path)

    return collage_path

def upload_zip(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo_upload = form.save()
            zip_file_path = photo_upload.zip_file.path

            try:
                file_count = len(zipfile.ZipFile(zip_file_path, 'r').namelist())
                grid_size = int(file_count ** 0.5)
                collage_path = handle_zip_file(zip_file_path, grid_size)
                collage_url = settings.MEDIA_URL + 'collage.jpg'
                return render(request, 'collage/collage.html', {'collage_url': collage_url})
            except Exception as e:
                return render(request, 'collage/upload.html', {'form': form, 'error': str(e)})
    else:
        form = PhotoUploadForm()
    return render(request, 'collage/upload.html', {'form': form})
