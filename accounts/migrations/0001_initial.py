# Generated by Django 3.2.25 on 2024-09-25 13:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='email address')),
                ('is_admin', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=50)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='user/')),
                ('mobile_number', models.CharField(max_length=20, unique=True)),
                ('accepted_policy', models.BooleanField(default=False)),
                ('email_otp', models.CharField(blank=True, max_length=6, null=True)),
                ('sms_otp', models.CharField(blank=True, max_length=6, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
