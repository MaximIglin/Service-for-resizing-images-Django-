import os
import urllib
from tempfile import NamedTemporaryFile

from PIL import Image as Pil_image
from django.db import models
from django.core.files import File


class Image(models.Model):
    """This model is describe all images"""
    name = models.CharField("Название изображения", max_length=150, null=True, blank=True)
    url = models.URLField("Ссылка на изображение", null=True, blank=True)
    picture = models.ImageField(null=True, blank=True)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    parent = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):

        if self.url and not self.picture:
            temporary_image = NamedTemporaryFile(delete=True)
            temporary_image.write(urllib.request.urlopen(self.url).read())
            temporary_image.flush()
            self.picture.save(os.path.basename(self.url), File(temporary_image))
            self.name = str(self.picture)
            self.width, self.height = Pil_image.open(self.picture).size   # Получаем размеры изображения

        elif (self.picture and self.url) or (self.picture and not self.url):
            self.name = str(self.picture)
            self.width, self.height = Pil_image.open(self.picture).size   # Получаем размеры изображения

        super(Image, self).save(*args, *kwargs)

    def delete(self, *args, **kwargs):

        storage, path = self.picture.storage, self.picture.path
        super(Image, self).delete(*args, **kwargs)
        storage.delete(path)

    class Meta:
        verbose_name = "Изображения"
        ordering = ['id']

    def __str__(self):
        return f"{self.id}: {self.name}"
