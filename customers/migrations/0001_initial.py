# Generated by Django 4.2.1 on 2023-08-01 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('website', models.URLField(blank=True)),
                ('address', models.TextField(blank=True)),
                ('employees', models.PositiveIntegerField(default=0)),
                ('industry', models.CharField(blank=True, max_length=100)),
                ('company_type', models.CharField(blank=True, max_length=100)),
                ('linkedin_profile', models.URLField(blank=True)),
                ('twitter_profile', models.URLField(blank=True)),
                ('facebook_profile', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('address', models.TextField(blank=True)),
                ('company_name', models.CharField(blank=True, max_length=200)),
                ('job_title', models.CharField(blank=True, max_length=100)),
                ('website', models.URLField(blank=True)),
                ('industry', models.CharField(blank=True, max_length=100)),
                ('linkedin_profile', models.URLField(blank=True)),
                ('twitter_profile', models.URLField(blank=True)),
                ('facebook_profile', models.URLField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('due_date', models.DateField()),
                ('is_completed', models.BooleanField(default=False)),
                ('priority', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Medium', max_length=10)),
                ('category', models.CharField(choices=[('Follow-up', 'Follow-up'), ('Meeting', 'Meeting'), ('Call', 'Call'), ('Email', 'Email')], default='Follow-up', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('note_type', models.CharField(choices=[('General', 'General'), ('Meeting', 'Meeting'), ('Call', 'Call'), ('Follow-up', 'Follow-up')], default='General', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('closing_date', models.DateField()),
                ('is_won', models.BooleanField(default=False)),
                ('stage', models.CharField(choices=[('Prospect', 'Prospect'), ('Qualification', 'Qualification'), ('Negotiation', 'Negotiation'), ('Closed Won', 'Closed Won'), ('Closed Lost', 'Closed Lost')], default='Prospect', max_length=100)),
                ('probability', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.company')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('role', models.CharField(choices=[('Decision Maker', 'Decision Maker'), ('Influencer', 'Influencer'), ('Gatekeeper', 'Gatekeeper')], default='Decision Maker', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
            ],
        ),
    ]
