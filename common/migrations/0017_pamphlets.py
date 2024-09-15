# Generated by Django 5.0.7 on 2024-09-03 12:48

import taggit.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0016_rename_content_article_description_and_more'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pamphlets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='زمان ثبت')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('special', models.BooleanField(default=False, verbose_name='آیا این دوره ویژه هست؟')),
                ('img', models.ImageField(upload_to='image', verbose_name='تصویر')),
                ('word', models.FileField(upload_to='text', verbose_name='فایل وورد')),
                ('pdf', models.FileField(upload_to='text', verbose_name='فایل پی دی اف')),
                ('amount', models.DecimalField(decimal_places=3, max_digits=15, verbose_name='مبلغ')),
                ('category', models.ManyToManyField(related_name='pamphlets', to='common.category', verbose_name='دسته بندی ')),
                ('tag', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name_plural': 'جزوات',
            },
        ),
    ]
