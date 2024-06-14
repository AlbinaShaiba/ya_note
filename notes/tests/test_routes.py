from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.not_author = User.objects.create(username='Читатель')
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)
        cls.note = Note.objects.create(title='Заголовок',
                                       text='Текст',
                                       slug='Slug',
                                       author=cls.author)
        
        cls.LOGIN_URL_REVERSE = reverse('users:login')
        cls.LOGOUT_URL_REVERSE = reverse('users:logout')
        cls.SIGNUP_URL_REVERSE = reverse('users:signup')
        cls.HOME_URL_REVERSE = reverse('notes:home')
        cls.NOTES_URL_REVERSE = reverse('notes:list')
        cls.DETAIL_URL_REVERSE = reverse('notes:detail', args=(cls.note.slug,))
        cls.NOTE_ADD_URL_REVERSE = reverse('notes:add')
        cls.EDIT_URL_REVERSE = reverse('notes:edit', args=(cls.note.slug,))
        cls.DELETE_URL_REVERSE = reverse('notes:delete', args=(cls.note.slug,))
        cls.SUCCESS_URL_REVERSE = reverse('notes:success')



    def test_page_availability_for_anonymous_user(self):
        urls = (
            self.HOME_URL_REVERSE,
            self.LOGIN_URL_REVERSE,
            self.LOGOUT_URL_REVERSE,
            self.SIGNUP_URL_REVERSE,
        )

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        urls = (
            self.NOTES_URL_REVERSE,
            self.NOTE_ADD_URL_REVERSE,
            self.SUCCESS_URL_REVERSE,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.auth_client.get(url)
                assert response.status_code == HTTPStatus.OK

    def test_availability_for_different_users(self):
        users_statuses = (
            (self.auth_client, HTTPStatus.OK),
            (self.not_author_client, HTTPStatus.NOT_FOUND),)
        for user, status in users_statuses:
            for url in (self.EDIT_URL_REVERSE,
                        self.DELETE_URL_REVERSE,
                        self.DETAIL_URL_REVERSE):
                with self.subTest(client=user, url=url):
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect(self):
        login_url = reverse('users:login')
        urls = (
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
            ('notes:detail', (self.note.slug,)),
            ('notes:add', None),
            ('notes:success', None),
            ('notes:list', None),
        )

        for name, arg in urls:
            with self.subTest(name=name):
                url = reverse(name, args=arg)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
