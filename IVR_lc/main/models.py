from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """Модель пользователя начальная"""
    fullname = models.CharField(max_length=127)
    age = models.IntegerField(null=True)
    isteacher = models.IntegerField(null=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

# Create your models here.
class Theory(models.Model):
    """"
        Модель пакета теоретических материалов
        :param user: Пользователь, который создал работу
        :param picture: Картинка работы(превью)
        :param name: Название работы
        :param description: Описание работы
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    file = models.FileField(blank=True,upload_to='static/files')
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
