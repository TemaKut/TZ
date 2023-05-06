from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BooksViewSet


app_name = 'api'

# Роутер для регистрации view-sets
router_v1 = DefaultRouter()
router_v1.register('books', BooksViewSet, basename='books')


# Список urls приложения
urlpatterns = [
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include('djoser.urls.base')),
    path('v1/', include(router_v1.urls)),
]
