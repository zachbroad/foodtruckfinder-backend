# Generated by Django 3.0.6 on 2020-07-25 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('trucks', '0001_initial'),
        ('catering', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='caterrequest',
            name='truck',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='trucks.Truck'),
        ),
    ]
