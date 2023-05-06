from rest_framework import serializers as ser

from .models import Book


class BookSerializer(ser.ModelSerializer):
    """ Сериализатор модели книги. """

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('id', 'author', 'published_at')

    def create(self, validated_data):
        """ Переопределение метода создания книги в БД """
        validated_data['author'] = self.context.get('request').user

        return super().create(validated_data)
