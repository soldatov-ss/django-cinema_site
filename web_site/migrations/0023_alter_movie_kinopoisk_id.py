# Generated by Django 4.0.1 on 2022-03-28 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_site', '0022_movie_kinopoisk_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='kinopoisk_id',
            field=models.IntegerField(default=0, unique=True, verbose_name='Кинопоиск ID'),
        ),
    ]
