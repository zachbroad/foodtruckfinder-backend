# Generated by Django 3.0.6 on 2020-07-28 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='route',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='webview_route',
            field=models.URLField(blank=True, null=True),
        ),
    ]
