# Generated by Django 3.0.6 on 2020-07-19 01:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trucks', '0006_auto_20200625_0114'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CancelledEvent',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('events.event',),
        ),
        migrations.RemoveField(
            model_name='event',
            name='endDate',
        ),
        migrations.RemoveField(
            model_name='event',
            name='frequency',
        ),
        migrations.RemoveField(
            model_name='event',
            name='start_date',
        ),
        migrations.AddField(
            model_name='event',
            name='date',
            field=models.DateField(null=True, verbose_name='Date'),
        ),
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_organizer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='truck',
            field=models.ManyToManyField(related_name='events', to='trucks.Truck'),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(blank=True, default='Sorry, this event has no description', max_length=500),
        ),
    ]