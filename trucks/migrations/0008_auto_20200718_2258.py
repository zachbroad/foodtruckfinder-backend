# Generated by Django 3.0.5 on 2020-07-19 02:58

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trucks', '0007_truck_available_for_catering'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Like',
            new_name='ReviewLike',
        ),
    ]