# Generated by Django 3.0.2 on 2020-01-19 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trucks', '0004_auto_20200119_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='truck',
            name='openning_times',
            field=models.ManyToManyField(null=True, to='trucks.OpenningTime'),
        ),
    ]
