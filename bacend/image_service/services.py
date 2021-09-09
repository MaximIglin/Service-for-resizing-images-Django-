from .models import Image
from PIL import Image as Pil_image
import sys
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile 


def get_image_by_id(id):
    """This fuction is return image by their id"""
    return Image.objects.get(id=id)


def resize_image(first_image, width, height):
        temp_image = ((Pil_image.open(first_image.picture)).convert("RGB")).resize((width, height), Pil_image.ANTIALIAS)
        filestream = BytesIO()
        temp_image.save(filestream, 'JPEG', quality=90)
        filestream.seek(0)
        name = f"{str(first_image.picture).split('.')[0]}_{width}_{height}.{str(first_image.picture).split('.')[1]}"
        image = InMemoryUploadedFile(filestream, 'picture', name, 'jpeg/image', sys.getsizeof(filestream), None )
        return image    
