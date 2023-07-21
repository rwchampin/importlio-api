# Generated by Django 4.2.1 on 2023-07-18 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proxies', '0002_alter_proxy_anonymity_level_alter_proxy_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proxy',
            name='protocols',
        ),
        migrations.AddField(
            model_name='proxy',
            name='http',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='proxy',
            name='https',
            field=models.BooleanField(default=False),
        ),
    ]
