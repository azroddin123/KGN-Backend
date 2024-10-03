# Generated by Django 3.2.25 on 2024-10-03 08:42

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('category_name', models.CharField(max_length=128)),
                ('category_image', models.ImageField(blank=True, null=True, upload_to='category/')),
                ('category_description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('store_name', models.CharField(default='Store 1', max_length=256)),
                ('store_address', models.CharField(blank=True, max_length=256, null=True)),
                ('pincode', models.CharField(blank=True, max_length=6, null=True)),
                ('store_admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=258)),
                ('category_image', models.ImageField(blank=True, null=True, upload_to='sub_category/')),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.category')),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StorePincode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pincode', models.CharField(max_length=6)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pincodes', to='products.store')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('product_name', models.CharField(max_length=128)),
                ('product_image', models.ImageField(blank=True, null=True, upload_to='product/')),
                ('price', models.PositiveIntegerField()),
                ('stock', models.PositiveIntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('sub_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.subcategory')),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.PositiveIntegerField(default=0)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='products.product')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='products.store')),
            ],
            options={
                'unique_together': {('store', 'product')},
            },
        ),
    ]
