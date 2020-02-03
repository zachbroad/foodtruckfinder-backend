# Generated by Django 3.0.2 on 2020-01-19 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trucks', '0005_auto_20200119_1248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='truck',
            name='openning_times',
        ),
        migrations.AddField(
            model_name='openningtime',
            name='truck',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='trucks.Truck'),
            preserve_default=False,
        ),
    ]