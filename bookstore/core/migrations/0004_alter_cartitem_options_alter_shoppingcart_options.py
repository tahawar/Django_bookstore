# Generated by Django 5.0.6 on 2024-06-22 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_purchase_purchaseitem_shoppingcart_cartitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitem',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'ordering': ['id']},
        ),
    ]
