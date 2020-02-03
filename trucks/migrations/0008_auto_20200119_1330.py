# Generated by Django 3.0.2 on 2020-01-19 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trucks', '0007_auto_20200119_1310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='truck',
            name='openning_times',
        ),
        migrations.AddField(
            model_name='truck',
            name='openning_times',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='trucks.OpenningTime'),
        ),
    ]