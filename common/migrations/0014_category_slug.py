# Generated by Django 5.0.7 on 2024-08-13 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0013_alter_category_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, verbose_name='اسلاگ'),
        ),
    ]
