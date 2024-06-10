from datetime import datetime, timedelta
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import WARNING
from notes.models import Note


User = get_user_model()


class TestNoteCreation(TestCase):
    NOTE_TITLE = 'Заметка'
    NOTE_TEXT = 'Текст заметки'
    NOTE_SLUG = 'slug'
    NOTE_DATE = today


    @classmethod
    def setUpTestData(cls):
        today = datetime.today()
        cls.note = Note.objects.create(title='Заметка',
                                       text='Текст заметки',
                                       slug='slug',
                                       author=cls.author,
                                       date=today)
        cls.url = reverse('notes:detail', args=(cls.note.slug,))
        cls.user = User.objects.create(username='Юзер')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.form_data = {
            'title': cls.NOTE_TITLE,
            'text': cls.NOTE_TEXT,
            'slug': cls.NOTE_SLUG,
            'date': cls.NOTE_DATE
        }
        