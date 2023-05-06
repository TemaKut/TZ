from django.db import models as m

from users.models import User


class Book(m.Model):
    """ Модель БД. Книга. """

    title = m.CharField(
        verbose_name='Название книги.',
        max_length=250,
        unique=True,
    )
    description = m.TextField(
        verbose_name='Описание книги'
    )
    published_at = m.DateTimeField(
        verbose_name='Дата и время публикации книги.',
        auto_now=True,
    )
    author = m.ForeignKey(
        verbose_name='Автор книги.',
        to=User,
        on_delete=m.CASCADE,
    )

    def __str__(self):
        """ Строчное представление объекта книги """
        class_name = self.__class__.__name__

        return f'{class_name}<id={self.pk}, title={self.title}>'
