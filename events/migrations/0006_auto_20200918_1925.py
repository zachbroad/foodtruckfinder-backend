# Generated by Django 3.0.5 on 2020-09-18 23:25

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0005_auto_20200918_1844'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='imgoing',
            unique_together={('event', 'user')},
        ),
    ]
