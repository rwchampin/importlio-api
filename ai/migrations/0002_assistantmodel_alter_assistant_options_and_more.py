# Generated by Django 4.2.1 on 2023-12-03 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssistantModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['updated_at', 'name'],
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='assistant',
            options={'ordering': ['updated_at', 'name']},
        ),
        migrations.AlterModelOptions(
            name='chatroom',
            options={'ordering': ['updated_at', 'name']},
        ),
    ]
