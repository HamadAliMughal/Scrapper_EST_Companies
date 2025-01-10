# Generated by Django 5.1.4 on 2025-01-03 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('Company_Name', models.CharField(max_length=255, unique=True)),
                ('Emails', models.TextField(blank=True, null=True)),
                ('Phones', models.TextField(blank=True, null=True)),
                ('Website', models.URLField(blank=True, null=True)),
                ('Created_At', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
