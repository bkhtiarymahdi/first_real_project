# Generated by Django 5.0.7 on 2024-08-08 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0011_quoteimage_title_alter_movie_duration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inpersoncourse',
            name='img',
            field=models.ImageField(default=10000, upload_to='image', verbose_name='تصویر'),
            preserve_default=False,
        ),
    ]
