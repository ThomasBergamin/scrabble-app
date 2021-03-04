# Generated by Django 3.1.7 on 2021-02-25 09:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scrabble', '0008_auto_20210225_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='heure',
            field=models.TimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 2, 25, 9, 44, 11, 685455, tzinfo=utc)),
        ),
    ]
