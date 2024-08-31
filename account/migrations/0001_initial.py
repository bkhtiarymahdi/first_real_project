# Generated by Django 5.0.1 on 2024-07-01 05:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='زمان ثبت')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='image/', verbose_name='تصویر صورت')),
                ('city', models.CharField(blank=True, choices=[('tehran', 'تهران'), ('razavi', 'خراسان رضوی'), ('fars', 'فارس'), ('esfahan', 'اصفهان'), ('A sharqi', 'آذربایجان شرقی'), ('A qarbi', 'آذربایجان غربی'), ('khozestan', 'خوزستان'), ('mazandaran', 'مازندران'), ('kerman', 'کرمان'), ('sistan', 'سیستان و بلوچستان'), ('alborz', 'البرز'), ('gilan', 'گیلان'), ('kermansha', 'کرمانشاه'), ('golestan', 'گلستان'), ('lorestan', 'لرستان'), ('hormozgan', 'هرمزگان'), ('hamedan', 'همدان'), ('kordestan', 'کردستان'), ('qom', 'قم'), ('markazi', 'مرکزی'), ('qazvin', 'قزوین'), ('ardebil', 'اردبیل'), ('yazd', 'یزد'), ('boshehr', 'بوشهر'), ('zanjan', 'زنجان'), ('bakhtiary', 'چهارمحال بختیاری'), ('KH jonobi', 'خراسان جنوبی'), ('KH shomali', 'خراسان شمالی'), ('boyerahmad', 'کهکیلویه و بویر احمد'), ('semnan', 'سمنان'), ('ilam', 'ایلام')], max_length=250, null=True, verbose_name='شهر محل سکونت')),
                ('full_address', models.CharField(blank=True, max_length=250, null=True, verbose_name='ادرس محل سکونت')),
                ('special_user', models.BooleanField(default=False, verbose_name='کاربر ویژه')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name_plural': 'کاربر ها',
            },
        ),
    ]
