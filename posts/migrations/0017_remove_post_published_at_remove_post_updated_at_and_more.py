# Generated by Django 4.2.1 on 2023-07-26 18:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0016_auto_20230726_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='published_at',
        ),
        migrations.RemoveField(
            model_name='post',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='post',
            name='published',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]