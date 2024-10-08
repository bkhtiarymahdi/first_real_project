# Generated by Django 5.0.7 on 2024-08-05 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_alter_quoteimage_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='quoteimage',
            name='title',
            field=models.CharField(default='ایران', max_length=20, verbose_name='عنوان'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='movie',
            name='duration',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='زمان فیلم'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='film',
            field=models.FileField(upload_to='movie', verbose_name='بارگزاری فیلم'),
        ),
    ]
