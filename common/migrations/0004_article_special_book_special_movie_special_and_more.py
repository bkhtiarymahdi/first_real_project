# Generated by Django 5.0.6 on 2024-06-11 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_book_tag_movie_tag_voice_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='special',
            field=models.BooleanField(default=False, verbose_name='آیا این مقاله ویژه هست؟'),
        ),
        migrations.AddField(
            model_name='book',
            name='special',
            field=models.BooleanField(default=False, verbose_name='آیا این مقاله ویژه هست؟'),
        ),
        migrations.AddField(
            model_name='movie',
            name='special',
            field=models.BooleanField(default=False, verbose_name='آیا این مقاله ویژه هست؟'),
        ),
        migrations.AddField(
            model_name='voice',
            name='special',
            field=models.BooleanField(default=False, verbose_name='آیا این مقاله ویژه هست؟'),
        ),
    ]
