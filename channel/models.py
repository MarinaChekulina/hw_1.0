import datetime

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='users_prof', on_delete=models.CASCADE, primary_key=True)
    avatar = models.ImageField(verbose_name="Аватар")


class Channel(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=100, verbose_name="Название")
    image = models.ImageField(upload_to='uploads/', default='uploads/default_avatar.jpg', verbose_name="Картинка")
    category = models.CharField(max_length=50, verbose_name='Категория')
    text = models.TextField(verbose_name="Текст")
    video = models.TextField(verbose_name="Ссылка на видео")
    date = models.DateField(default=datetime.datetime.now, verbose_name="Дата создания")
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")
    user_subscription = models.ManyToManyField(User, through='Subscription', related_name='users')

    def __str__(self):
        return self.title


# Подписка
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)

    class Meta:
        unique_together = ("user", "channel")


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
