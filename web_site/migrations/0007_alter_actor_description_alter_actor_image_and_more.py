# Generated by Django 4.0.1 on 2022-02-21 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_site', '0006_reviews_created_at_alter_movieshots_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='image',
            field=models.ImageField(blank=True, upload_to='actors/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='tagline',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Слоган'),
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]
