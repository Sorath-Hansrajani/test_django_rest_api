# Create your models here.
from django.db import models
from django.conf import settings


# lets us explicitly set upload path and filename
def upload_to(instance, filename):
    return settings.MEDIA_ROOT+settings.MEDIA_URL+'{filename}'.format(filename=filename)


class Person(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False)
    image_url = models.ImageField(upload_to=upload_to, blank=False, null=False)

    def __str__(self):
        return self.name

