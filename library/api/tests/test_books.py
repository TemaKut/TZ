from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from users.models import User
from books.models import Book


class TestBooksApi(APITestCase):
    """ Тестирование эндпоинтов книг. """

    @classmethod
    def setUpClass(cls):
        """ Выполнить единажды перед тестами. """
        super().setUpClass()

        cls.authorized_user = APIClient()
        cls.another_authorized_user = APIClient()
        cls.user = User.objects.create(
            username='TestUser',
            email='test@example.com',
            first_name='Test_first_name',
            last_name='Test_last_name',
            password='test_password123',
        )
        cls.another_user = User.objects.create(
            username='anotherTestUser',
            email='anothertest@example.com',
            first_name='anotherTest_first_name',
            last_name='anotherTest_last_name',
            password='anothertest_password123',
        )
        # Авторизованный клиент
        cls.authorized_user.force_authenticate(user=cls.user)
        # Второстепенный авторизованный клиент
        cls.another_authorized_user.force_authenticate(user=cls.another_user)
        # Неавторизованный клиент
        cls.client = APIClient()

        # ___URI`s___
        cls.books_url = reverse('api:books-list')
        cls.book_url = lambda self, id: reverse('api:books-detail', args=(id,))

    def test_create_book(self):
        """ Создание книги авторизованным пользователем """
        start_count_books = len(Book.objects.all())

        title = "Test_title"
        description = "Test_descr"

        response = self.authorized_user.post(
            path=self.books_url,
            data={
                "title": title,
                "description": description,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(start_count_books + 1, len(Book.objects.all()))

        created_book = Book.objects.first()

        self.assertEqual(created_book.title, title)
        self.assertEqual(created_book.description, description)

        author_id = created_book.author.id

        self.assertEqual(author_id, self.user.id)

    def test_create_book_by_unauthorized_client(self):
        """ Создание книги неавторизованным клиентом """
        data = {
            "title": 'Title',
            "description": 'description',
        }

        with self.assertRaises(ValueError):
            self.client.post(path=self.books_url, data=data),

    def test_get_all_books(self):
        """ Получение всех книг авторизованным пользователем. """
        need_books = 10

        for i in range(need_books):
            Book.objects.create(
                title=f'title{i}',
                description=f'descr{i}',
                author=self.user,
            )

        self.assertEqual(len(Book.objects.all()), need_books)

        response = self.authorized_user.get(path=self.books_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), need_books)

    def test_get_all_books_by_unauthorized_client(self):
        """ Получение всех книг не авторизованным пользователем. """
        need_books = 10

        for i in range(need_books):
            Book.objects.create(
                title=f'title{i}',
                description=f'descr{i}',
                author=self.user,
            )

        self.assertEqual(len(Book.objects.all()), need_books)

        response = self.client.get(path=self.books_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), need_books)

    def test_user_cant_change_books_created_by_another_user(self):
        """ Пользователь не может изменять книги другого пользоваетля. """
        self.assertEqual(len(Book.objects.all()), 0)
        Book.objects.create(
            title='another_title',
            description='another_descr',
            author=self.another_user,
        )
        self.assertEqual(len(Book.objects.all()), 1)

        response = self.authorized_user.patch(
            path=self.book_url(1),
            data={'title': 'changed_title'},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_change_his_books(self):
        """ Пользователь может менять свои книги. """
        self.assertEqual(len(Book.objects.all()), 0)
        Book.objects.create(
            title='title',
            description='descr',
            author=self.user,
        )
        self.assertEqual(len(Book.objects.all()), 1)

        title = 'changed_title'
        response = self.authorized_user.patch(
            path=self.book_url(1),
            data={'title': title},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book = Book.objects.first()

        self.assertEqual(book.title, title)
