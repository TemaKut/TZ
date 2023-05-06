from rest_framework.viewsets import ModelViewSet

from books.models import Book
from books.serializers import BookSerializer
from books.permissions import OnlyAuthorizedUserCanChangeBooks


class BooksViewSet(ModelViewSet):
    """ ViewSet эндпоинтов модели книги. """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [OnlyAuthorizedUserCanChangeBooks]
