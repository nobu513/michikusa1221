# Generated by Django 3.1.4 on 2020-12-24 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fts_app', '0002_docddata_junban'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docddata',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
