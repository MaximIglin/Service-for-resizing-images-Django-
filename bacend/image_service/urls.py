from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import AllImagesViewSet, ImageDetailApi, ResizeImage

router = SimpleRouter()

urlpatterns = [
    path('api/images/', AllImagesViewSet.as_view()),
    path('api/images/<int:pk>/', ImageDetailApi.as_view()),
    path('api/images/<int:pk>/resize/', ResizeImage.as_view())
    
]
urlpatterns += router.urls