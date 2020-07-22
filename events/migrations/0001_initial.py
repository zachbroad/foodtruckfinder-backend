# Generated by Django 3.0.4 on 2020-05-26 17:52

from django.db import migrations, models
import django_google_maps.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.CharField(blank=True, default='Sorry, this truck has no description', max_length=500)),
                ('address', django_google_maps.fields.AddressField(blank=True, max_length=200, null=True, verbose_name='address')),
                ('geolocation', django_google_maps.fields.GeoLocationField(blank=True, max_length=100, null=True, verbose_name='geolocation')),
                ('frequency', models.IntegerField(choices=[(0, 'None'), (1, 'Daily'), (7, 'Weekly'), (14, 'Biweekly')])),
                ('start_time', models.TimeField(verbose_name='Start Time')),
                ('end_time', models.TimeField(verbose_name='End Time')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('cancelledDate', models.DateField(blank=True, null=True, verbose_name='Cancelled Date')),
            ],
        ),
    ]
