# Generated by Django 3.0.6 on 2020-07-25 00:58

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
                ('address', django_google_maps.fields.AddressField(blank=True, max_length=200, null=True, verbose_name='address')),
                ('geolocation', django_google_maps.fields.GeoLocationField(blank=True, max_length=100, null=True, verbose_name='geolocation')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True, default='Sorry, this event has no description', max_length=3000)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('cancelled_date', models.DateField(blank=True, null=True, verbose_name='Cancelled Date')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
