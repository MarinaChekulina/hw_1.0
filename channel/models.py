import datetime

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(verbose_name="Аватар")


class Channel(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=100, verbose_name="Название")
    image = models.ImageField(upload_to='uploads/', default='uploads/default_avatar.jpg', verbose_name="Картинка")
    text = models.TextField(verbose_name="Текст")
    video = models.TextField(verbose_name="Видео")
    date = models.DateField(default=datetime.datetime.now, verbose_name="Дата создания")
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")


class Comment(models.Model):
    author = models.ForeignKey(User)
    channel = models.ForeignKey(Channel)
    text = models.TextField(verbose_name="Текст")
    date = models.DateField(default=datetime.datetime.now, verbose_name="Дата создания")


# связь многие ко многим
class Like(models.Model):
    user = models.ForeignKey(User)
    channel = models.ForeignKey(Channel)
    like = models.BooleanField(default=True)

    # вложенный класс в класс Like
    class Meta:
        unique_together = ("user", "channel")
