# Generated by Django 5.0.7 on 2024-09-07 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0018_remove_article_amount_order_orderitem_transaction_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user_access',
            options={'verbose_name_plural': 'دسترسی های کاربر به دوره ها'},
        ),
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='جمع مبالغ'),
        ),
    ]
