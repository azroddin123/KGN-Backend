# Generated by Django 3.2.25 on 2024-10-10 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_product_product_name'),
        ('orders', '0004_alter_cartitem_cart'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitem',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('cart', 'product')},
        ),
    ]
