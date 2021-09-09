from rest_framework.response import Response
from .serializers import ImageSerializer
from .models import Image
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView


from .services import get_image_by_id, resize_image


class AllImagesViewSet(APIView):
    """This viewset is return all images"""
    def get(self, request):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if "file" in request.data.keys() and "url" in request.data.keys():
            new_image = Image()
            new_image.picture = request.data['file']
            new_image.save()
            serializer = ImageSerializer(new_image)
            return Response(serializer.data)
        elif "url" in request.data.keys() and not "file" in request.data.keys():
            new_image = Image()
            new_image.url = request.data['url']
            new_image.save()
            serializer = ImageSerializer(new_image)
            return Response(serializer.data)            





class ImageDetailApi(APIView):
    """API for detail output of review"""
    def get(self,request,pk):
        image = get_image_by_id(pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data)
    def delete(self, request, pk):
        image = get_image_by_id(pk)
        image.delete()
        serializer = ImageSerializer(image)
        return Response()


class ResizeImage(APIView):
    """Api for resizing image"""

    def post(self, request, pk):
        resizing_image = Image()
        first_image = get_image_by_id(pk)

        #Получаем высоту и ширину из запроса
        print(request.data.keys())
        if ('width' in request.data.keys()) and ('height' in request.data.keys()):
            width = int(request.data['width'])
            height = int(request.data['height'])
            resizing_image.url = first_image.url
            resizing_image.width = width
            resizing_image.height = height
            resizing_image.parent = pk
            resizing_image.picture = resize_image(first_image, width, height)
            resizing_image.save()
        elif ('width' in request.data.keys()) and ('height' not in request.data.keys()):
            width = int(request.data['width'])
            height = first_image.height
            resizing_image.url = first_image.url
            resizing_image.width = width
            resizing_image.height = height
            resizing_image.parent = pk
            resizing_image.picture = resize_image(first_image, width, height)
            resizing_image.save()    
        elif ('width' not in request.data.keys()) and ('height' in request.data.keys()):
            width = first_image.width
            height = int(request.data['height'])
            resizing_image.url = first_image.url
            resizing_image.width = width
            resizing_image.height = height
            resizing_image.parent = pk
            resizing_image.picture = resize_image(first_image, width, height)
            resizing_image.save()                     

        
        serializer = ImageSerializer(resizing_image)
        return Response(serializer.data)
          

