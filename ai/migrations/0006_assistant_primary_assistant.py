# Generated by Django 4.2.1 on 2023-12-03 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0005_alter_assistant_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='assistant',
            name='primary_assistant',
            field=models.BooleanField(default=False),
        ),
    ]