import urllib
from urllib.error import URLError
import sys
from io import BytesIO

from PIL import Image as Pil_image, UnidentifiedImageError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response

from .serializers import ImageSerializer
from .models import Image


def add_new_image(request):
    """This function is return new created Image-object"""
    try:
        if ("url" in request.data.keys() and "file" in request.data.keys()):
           return Response({"__all__": "Two field"}, status=status.HTTP_400_BAD_REQUEST)
        if "file" in request.data.keys():
            new_image = Image()
            new_image.picture = request.data['file']
            new_image.save()
            return Response(ImageSerializer(new_image).data)
        elif "url" in request.data.keys() and "file" not in request.data.keys():
            try:
                urllib.request.urlopen(request.data['url'])
                new_image = Image()
                new_image.url = request.data['url']
                new_image.save()
                serializer = ImageSerializer(new_image)
                return Response(serializer.data)
            except URLError:
                return Response({"400": "There isn't image on this url!"}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({"400": "Please enter a valid url!"}, status=status.HTTP_400_BAD_REQUEST)
    except UnidentifiedImageError:
        return Response({"400": "Please put a photo!"}, status=status.HTTP_400_BAD_REQUEST)


def does_not_exist_decorator(function):
    """This decorator is needed in order to handle exceptions for non-existent instances"""
    def wrapped(self, request, pk):
        try:
            return function(self, request, pk)
        except ObjectDoesNotExist:
            return Response({"Error": "Image does not exist or was deleted"}, status=status.HTTP_404_NOT_FOUND)
    return wrapped


def get_image_by_id(id):
    """This fuction is return image by their id"""
    return Image.objects.get(id=id)


def resize_image(first_image, width, height):
    """This function is return resized image"""
    resizing_image = Image()
    temp_image = ((Pil_image.open(first_image.picture)).convert("RGB")).resize((width, height), Pil_image.ANTIALIAS)
    filestream = BytesIO()
    temp_image.save(filestream, 'JPEG', quality=90)
    filestream.seek(0)
    name = f"{str(first_image.picture).split('.')[0]}_{width}_{height}.{str(first_image.picture).split('.')[1]}"
    image = InMemoryUploadedFile(filestream, 'picture', name, 'jpeg/image', sys.getsizeof(filestream), None)
    resizing_image.url = first_image.url
    resizing_image.width = width
    resizing_image.height = height
    resizing_image.parent = first_image.id
    resizing_image.picture = image
    resizing_image.save()
    return resizing_image
