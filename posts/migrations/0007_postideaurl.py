# Generated by Django 4.2.1 on 2024-01-02 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_postrephrase_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostIdeaUrl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('subtitle', models.CharField(blank=True, max_length=255, null=True)),
                ('headline', models.CharField(blank=True, max_length=255, null=True)),
                ('shadowText', models.CharField(blank=True, max_length=300, null=True)),
                ('excerpt', models.TextField(blank=True, null=True)),
                ('seo_title', models.CharField(blank=True, max_length=400, null=True)),
                ('seo_description', models.TextField(blank=True, null=True)),
                ('seo_keywords', models.TextField(blank=True, null=True)),
                ('html', models.TextField()),
                ('current_segment', models.IntegerField(default=0)),
                ('segments', models.TextField(blank=True, null=True)),
            ],
        ),
    ]