# Generated by Django 3.2.25 on 2024-10-15 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_ordereditems_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='payment_status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
