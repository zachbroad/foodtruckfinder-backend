# Generated by Django 3.0.4 on 2020-05-21 19:18

from django.db import migrations, models
import django_google_maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_event_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='address',
            field=django_google_maps.fields.AddressField(blank=True, max_length=200, null=True, verbose_name='address'),
        ),
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.CharField(blank=True, default='Sorry, this truck has no description', max_length=500),
        ),
        migrations.AddField(
            model_name='event',
            name='geolocation',
            field=django_google_maps.fields.GeoLocationField(blank=True, max_length=100, null=True, verbose_name='geolocation'),
        ),
    ]
