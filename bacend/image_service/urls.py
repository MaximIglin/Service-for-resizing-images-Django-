from django.urls import path

from .views import AllImagesApi, ImageDetailApi, ResizeImage


urlpatterns = [
    path('api/images/', AllImagesApi.as_view()),
    path('api/images/<int:pk>/', ImageDetailApi.as_view()),
    path('api/images/<int:pk>/resize/', ResizeImage.as_view()) 
]
