from django.contrib import admin

from .models import User


# Добавление в админку модели БД..
admin.site.register(User)
