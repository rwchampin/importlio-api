# Generated by Django 4.2.1 on 2023-12-03 01:30

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_postoutlineitem_alter_post_post_type_postoutline_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='outline',
        ),
        migrations.AddField(
            model_name='postoutline',
            name='text',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='PostSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('subtitle', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='featured_images/')),
                ('content', models.TextField(blank=True, null=True)),
                ('html_id', models.CharField(blank=True, max_length=255, null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
        ),
    ]