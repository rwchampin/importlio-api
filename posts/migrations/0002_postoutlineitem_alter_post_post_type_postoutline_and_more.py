# Generated by Django 4.2.1 on 2023-12-01 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostOutlineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='posts.posttype'),
        ),
        migrations.CreateModel(
            name='PostOutline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('items', models.ManyToManyField(blank=True, to='posts.postoutlineitem')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='outline',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='posts.postoutline'),
        ),
    ]