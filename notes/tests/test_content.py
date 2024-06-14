from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note



User = get_user_model()


class TestNoteListPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.not_author = User.objects.create(username='Не автор')
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)
        cls.note = Note.objects.create(title='Заметка',
                                       text='Текст заметки',
                                       slug='slug',
                                       author=cls.author)
        
        cls.NOTES_URL_REVERSE = reverse('notes:list')
        cls.NOTE_ADD_URL_REVERSE = reverse('notes:add')
        cls.EDIT_URL_REVERSE = reverse('notes:edit', args=(cls.note.slug,))

    def test_note_in_list_for_author(self):
        response = self.auth_client.get(self.NOTES_URL_REVERSE)
        self.assertIn(self.note, response.context['object_list'])

    def test_note_in_list_for_not_author(self):
        response = self.not_author_client.get(self.NOTES_URL_REVERSE)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_create_and_edit_note_page_contains_form(self):
        urls = (
            self.NOTE_ADD_URL_REVERSE,
            self.EDIT_URL_REVERSE,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.auth_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)

