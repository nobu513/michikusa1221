# Generated by Django 3.1.4 on 2020-12-23 10:48

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DocDData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('doc', models.TextField()),
                ('book_id', models.CharField(max_length=100)),
                ('search_vector', django.contrib.postgres.search.SearchVectorField(null=True)),
                ('pages', models.TextField()),
            ],
        ),
        migrations.AddIndex(
            model_name='docddata',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search_vector'], name='fts_app_doc_search__7ab69a_gin'),
        ),
    ]
