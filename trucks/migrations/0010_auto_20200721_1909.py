# Generated by Django 3.0.5 on 2020-07-21 23:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('trucks', '0009_auto_20200721_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='live',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 21, 23, 9, 37, 159625, tzinfo=utc)),
        ),
    ]
