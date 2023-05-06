from django.contrib import admin

from .models import Book


# Регистрация моделей приложения в админке
admin.site.register(Book)
