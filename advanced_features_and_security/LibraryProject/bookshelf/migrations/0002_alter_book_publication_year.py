# Generated by Django 5.0.7 on 2024-08-25 19:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshelf', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publication_year',
            field=models.IntegerField(default=datetime.datetime(2024, 8, 25, 19, 56, 58, 789311, tzinfo=datetime.timezone.utc)),
        ),
    ]
