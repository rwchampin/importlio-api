# Generated by Django 4.2.1 on 2024-01-03 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_postideasegment_remove_postideaurl_segments_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='postrephrase',
            name='current_keywords',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='postrephrase',
            name='current_top_keyword',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='postrephrase',
            name='current_top_keyword_country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='postrephrase',
            name='current_top_keyword_position',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='postrephrase',
            name='current_top_keyword_volume',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='postrephrase',
            name='current_traffic',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='postrephrase',
            name='current_traffic_value',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='postrephrase',
            name='previous_keywords',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='postrephrase',
            name='previous_top_keyword',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='postrephrase',
            name='previous_top_keyword_country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='postrephrase',
            name='previous_top_keyword_position',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='postrephrase',
            name='previous_top_keyword_volume',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='postrephrase',
            name='previous_traffic',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='postrephrase',
            name='previous_traffic_value',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='postrephrase',
            name='status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='postrephrase',
            name='top_keyword_position_change',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='postrephrase',
            name='traffic_change',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='postrephrase',
            name='traffic_value_change',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
