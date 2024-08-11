# Generated by Django 5.0.7 on 2024-08-11 21:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshelf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.CharField(default='Unknown Author', max_length=100),
        ),
        migrations.AddField(
            model_name='book',
            name='title',
            field=models.CharField(default='Unknown title', max_length=200),
        ),
        migrations.AlterField(
            model_name='book',
            name='publication_year',
            field=models.IntegerField(default=datetime.datetime(2024, 8, 11, 21, 5, 32, 94057, tzinfo=datetime.timezone.utc)),
        ),
    ]
