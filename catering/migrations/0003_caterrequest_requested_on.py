# Generated by Django 3.0.5 on 2020-09-18 02:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('catering', '0002_caterrequest_truck'),
    ]

    operations = [
        migrations.AddField(
            model_name='caterrequest',
            name='requested_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]