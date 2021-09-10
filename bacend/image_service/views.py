from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .services import add_new_image, get_image_by_id, resize_image, does_not_exist_decorator
from .serializers import ImageSerializer
from .models import Image


class AllImagesApi(APIView):
    """This viewset is return all images"""
    def get(self, request):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request):
        return add_new_image(request)


class ImageDetailApi(APIView):
    """API for detail output of review"""
    @does_not_exist_decorator
    def get(self, request, pk):
        image = get_image_by_id(pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data)

    @does_not_exist_decorator
    def delete(self, request, pk):
        image = get_image_by_id(pk)
        image.delete()
        return Response({"OK": "image deleted successfully"})


class ResizeImage(APIView):
    """Api for resizing image"""
    @does_not_exist_decorator
    def post(self, request, pk):
        first_image = get_image_by_id(pk)
        try:
            if ('width' in request.data.keys()) and ('height' in request.data.keys()):
                width = int(request.data['width'])
                height = int(request.data['height'])
                resizing_image = resize_image(first_image, width, height)
                serializer = ImageSerializer(resizing_image)
                return Response(serializer.data)
            elif ('width' in request.data.keys()) and ('height' not in request.data.keys()):
                width = int(request.data['width'])
                height = first_image.height
                resizing_image = resize_image(first_image, width, height)
                serializer = ImageSerializer(resizing_image)
                return Response(serializer.data)
            elif ('width' not in request.data.keys()) and ('height' in request.data.keys()):
                width = first_image.width
                height = int(request.data['height'])
                resizing_image = resize_image(first_image, width, height)
                serializer = ImageSerializer(resizing_image)
                return Response(serializer.data)
        except ValueError:
            return Response({"400": "Please enter a valid width or height"}, status=status.HTTP_400_BAD_REQUEST)
