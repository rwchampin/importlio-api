# Generated by Django 4.2.1 on 2023-10-03 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(error_messages={'blank': 'Email is required', 'unique': 'Email already exists'}, max_length=254, unique=True)),
            ],
        ),
    ]