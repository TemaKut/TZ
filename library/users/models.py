from django.db import models as m
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """ Модель БД. Переопределённая модель пользователя. """
    first_name = m.CharField(
        verbose_name='Имя пользователя',
        max_length=50,
        blank=True,
        null=True,
    )
    last_name = m.CharField(
        verbose_name='Фамилия пользователя',
        max_length=50,
        blank=True,
        null=True,
    )
    birth_date = m.DateField(
        verbose_name='Дата рождения',
        blank=True,
        null=True,
    )

    def __str__(self):
        """ Строчное представление объекта пользователя. """
        class_name = self.__class__.__name__

        return f'{class_name}<id={self.pk}, username={self.username}>'
