from datetime import datetime, timedelta
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import WARNING
from notes.models import Note


User = get_user_model()


class TestNoteCreation(TestCase):
    today = datetime.today()
    NOTE_TITLE = 'Заметка'
    NOTE_TEXT = 'Текст заметки'
    NOTE_SLUG = 'slug'
    NOTE_DATE = today

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('notes:home')
        cls.user = User.objects.create(username='Юзер')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.form_data = {
            'title': cls.NOTE_TITLE,
            'text': cls.NOTE_TEXT,
            'slug': cls.NOTE_SLUG,
            'date': cls.NOTE_DATE
        }


    def test_anonymous_user_cant_create_note(self):
        self.client.post(self.url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)
        
    def test_user_can_create_note(self):
        self.auth_client.force_login(self.user)
        self.auth_client.post(self.url, data=self.form_data)
        notes_count = Note.objects.count()
        print(self.auth_client)
        print(self.form_data)
        self.assertEqual(notes_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.text, self.NOTE_TEXT)
        self.assertEqual(note.author, self.user)
