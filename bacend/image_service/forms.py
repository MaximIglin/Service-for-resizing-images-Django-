from django import forms
from .models import Image


class ImageForm(forms.ModelForm):
    """This form for add images by url or file"""
    class Meta:
        model: Image
        fields = ['url','picture']