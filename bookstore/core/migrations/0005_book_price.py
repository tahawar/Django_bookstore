# Generated by Django 5.0.6 on 2024-06-22 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_cartitem_options_alter_shoppingcart_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.DecimalField(decimal_places=2, default=9.99, max_digits=10),
        ),
    ]
