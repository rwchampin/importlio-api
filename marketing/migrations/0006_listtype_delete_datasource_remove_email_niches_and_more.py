# Generated by Django 4.2.1 on 2023-09-30 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0005_remove_email_niche_remove_marketinglist_emails_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, null=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='DataSource',
        ),
        migrations.RemoveField(
            model_name='email',
            name='niches',
        ),
        migrations.RemoveField(
            model_name='marketinglist',
            name='fake',
        ),
        migrations.RemoveField(
            model_name='marketinglist',
            name='niches',
        ),
        migrations.RemoveField(
            model_name='marketingstatistic',
            name='niche',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='niches',
        ),
        migrations.AddField(
            model_name='email',
            name='marketing_list',
            field=models.ManyToManyField(related_name='email_marketing_list', to='marketing.marketinglist'),
        ),
        migrations.AddField(
            model_name='marketinglist',
            name='emails',
            field=models.ManyToManyField(related_name='marketing_list_emails', to='marketing.email'),
        ),
        migrations.AddField(
            model_name='marketinglist',
            name='slug',
            field=models.SlugField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='marketinglist',
            name='tags',
            field=models.ManyToManyField(related_name='tags', to='marketing.tag'),
        ),
        migrations.AddField(
            model_name='marketingstatistic',
            name='marketing_list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='statistics', to='marketing.marketinglist'),
        ),
        migrations.AddField(
            model_name='tag',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='Niche',
        ),
        migrations.AddField(
            model_name='marketinglist',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='type', to='marketing.listtype'),
        ),
    ]
