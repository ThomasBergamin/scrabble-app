# Generated by Django 3.1.7 on 2021-02-26 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrabble', '0015_auto_20210226_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='gagnant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrabble.player'),
        ),
    ]
