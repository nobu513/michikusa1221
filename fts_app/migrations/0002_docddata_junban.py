# Generated by Django 3.1.4 on 2020-12-24 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fts_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='docddata',
            name='junban',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
