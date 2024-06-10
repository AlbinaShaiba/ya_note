# Generated by Django 3.2.15 on 2024-06-10 07:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': ('-date',)},
        ),
        migrations.AddField(
            model_name='note',
            name='date',
            field=models.DateField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.CharField(default='Название заметки', help_text='Дайте короткое название заметке', max_length=100, verbose_name='Заголовок'),
        ),
    ]