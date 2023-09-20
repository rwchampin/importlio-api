# Generated by Django 4.2.1 on 2023-09-20 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_posttopicideas_alter_post_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='theme',
        ),
        migrations.AddField(
            model_name='post',
            name='headline_text_theme',
            field=models.CharField(choices=[('dark', 'Dark'), ('light', 'Light')], default='light', max_length=20),
        ),
        migrations.AddField(
            model_name='post',
            name='shadow_text_theme',
            field=models.CharField(choices=[('dark', 'Dark'), ('light', 'Light')], default='light', max_length=20),
        ),
        migrations.AddField(
            model_name='post',
            name='subtitle_text_theme',
            field=models.CharField(choices=[('dark', 'Dark'), ('light', 'Light')], default='light', max_length=20),
        ),
        migrations.AddField(
            model_name='post',
            name='title_text_theme',
            field=models.CharField(choices=[('dark', 'Dark'), ('light', 'Light')], default='light', max_length=20),
        ),
    ]
