from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """Модель пользователя для хранения безопасной информации
    :param fullname: Полное имя пользователя(имя+фамилия)
    :param age: Возраст пользователя
    :param isteacher: Категория доступа к сайту
    :param user: Пользователь, к которому относится данная запись профиля
    """
    fullname = models.CharField(max_length=127)
    age = models.IntegerField(null=True)
    isteacher = models.IntegerField(null=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

# Create your models here.
class Theory(models.Model):
    """"
        Модель пакета теоретических материалов
        :param user: Пользователь, который создал работу
        :param file: Теоретические материалы
        :param name: Название работы
        :param description: Описание работы
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    file = models.FileField(blank=True,upload_to='static/files')
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)


class TheorySearcher(models.Model):
    """
        Модель подготовленной к поиску без регистра лабораторной работы
        :param theory - Ссылка на основную теорию
        :param name - название работы в нижнем регистре
        :param by - Полное имя автора работы
        :param email - Адрес электронной почты автора работы - для вопросов
    """
    theory = models.ForeignKey(to=Theory, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    by = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
