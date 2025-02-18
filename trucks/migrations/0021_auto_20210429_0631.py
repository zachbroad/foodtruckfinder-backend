# Generated by Django 3.1 on 2021-04-29 10:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('trucks', '0020_auto_20210429_0522'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='truck',
            options={'get_latest_by': 'last_updated'},
        ),
        migrations.AddField(
            model_name='truck',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
