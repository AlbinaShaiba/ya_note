from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note
from notes.forms import NoteForm


User = get_user_model()


class TestListPage(TestCase):

    HOME_URL = reverse('notes:list')


    @classmethod
    def setUpTestData(cls):
        today = datetime.today()
        all_notes = []
        cls.author = User.objects.create(username='Автор заметки')
        for index in range(settings.NOTES_COUNT_ON_HOME_PAGE + 1):
            
            notes = Note(title=f'Заметка {index}',
                         text='Текст заметки',
                         slug=f'slug{index}',
                         author=cls.author,
                         date=today - timedelta(days=index))
            all_notes.append(notes)
        Note.objects.bulk_create(all_notes)

    def test_new_count(self):
        self.client.force_login(self.author)
        response = self.client.get(self.HOME_URL)
        object_list = response.context['object_list']
        notes_count = object_list.count()
        self.assertEqual(notes_count, settings.NOTES_COUNT_ON_HOME_PAGE)


    def test_notes_order(self):
        self.client.force_login(self.author)
        response = self.client.get(self.HOME_URL)
        object_list = response.context['object_list']
        all_dates = [note.date for note in object_list]
        sorted_dates = sorted(all_dates, reverse=True)
        self.assertEqual(all_dates, sorted_dates)



class TestDetailPage(TestCase):
    def setUpTestData(cls):
        today = datetime.today()
        cls.author = User.objects.create(username='Автор заметки')
        cls.reader = User.objects.create(username='Читатель')
        
        cls.note = Note(title=f'Заметка',
                         text='Текст заметки',
                         slug='slug',
                         author=cls.author,
                         date=today)
        cls.detail_url = reverse('notes:detail', args=(cls.note.slug,))

    def test_anonymous_client_has_no_form(self):
        response = self.client.get(self.detail_url)
        self.assertNotIn('form', response.context)


    def test_authorized_client_has_no_form(self):
        self.client.force_login(self.author)
        response = self.client.get(self.detail_url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
