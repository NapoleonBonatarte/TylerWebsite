# Generated by Django 4.1.7 on 2023-04-18 02:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_element'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.RemoveField(
            model_name='book',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='bookinstance',
            name='book',
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.DeleteModel(
            name='BookInstance',
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
    ]
