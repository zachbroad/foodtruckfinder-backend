# Generated by Django 3.0.2 on 2020-02-06 20:05

from django.db import migrations
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('trucks', '0026_auto_20200206_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='truck',
            name='phone',
            field=phone_field.models.PhoneField(blank=True, help_text='Contact number', max_length=31),
        ),
    ]
