# Generated by Django 4.2.1 on 2023-12-03 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0008_alter_chatroom_options_remove_chatmessage_chatroom_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
