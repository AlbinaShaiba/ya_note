from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.reader = User.objects.create(username='Читатель')
        cls.note = Note.objects.create(title='Заголовок',
                                       text='Текст',
                                       slug='Slug',
                                       author = cls.author)
        

    def test_page_availability_for_anonymous_user(self):
        urls = (
            ('notes:home', None),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
        )

        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        urls = (
            ('notes:list', None),
            ('notes:add', None),
            ('notes:success', None),
        )
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                assert response.status_code == HTTPStatus.OK


    def test_availability_for_different_users(self):
        users_statuses = (
                (self.author, HTTPStatus.OK),
                (self.reader, HTTPStatus.NOT_FOUND),
            )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in ('notes:edit', 'notes:delete', 'notes:detail'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect(self):
        login_url = reverse('users:login')
        for name in ('notes:edit', 'notes:delete', 'notes:detail',
                     'notes:add', 'notes:success', 'notes:list'):
            with self.subTest(name=name):
                url = reverse(name, args=(self.note.slug,))
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
