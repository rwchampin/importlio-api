# Generated by Django 4.2.1 on 2023-12-03 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0004_alter_assistant_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assistant',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='assistant',
            name='system_instructions',
            field=models.TextField(blank=True, null=True),
        ),
    ]
