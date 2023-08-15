# Generated by Django 4.2.1 on 2023-08-15 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_image_1',
        ),
        migrations.RemoveField(
            model_name='post',
            name='post_image_2',
        ),
        migrations.RemoveField(
            model_name='post',
            name='post_image_3',
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=50),
        ),
    ]