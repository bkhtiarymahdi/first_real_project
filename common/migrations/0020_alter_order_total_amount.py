# Generated by Django 5.0.7 on 2024-09-07 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0019_alter_user_access_options_alter_order_total_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=10, null=True, verbose_name='جمع مبالغ'),
        ),
    ]
