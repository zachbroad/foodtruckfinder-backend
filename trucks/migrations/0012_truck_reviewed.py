# Generated by Django 3.0.6 on 2020-10-13 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trucks', '0011_auto_20200923_1042'),
    ]

    operations = [
        migrations.AddField(
            model_name='truck',
            name='reviewed',
            field=models.BooleanField(default=False),
        ),
    ]
