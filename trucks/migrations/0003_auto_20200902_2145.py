# Generated by Django 3.0.6 on 2020-09-03 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trucks', '0002_auto_20200724_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='truck',
            name='image',
            field=models.ImageField(blank=True, default='assets/truck_logo_placeholder.png', upload_to='uploads/trucks/profile-pictures'),
        ),
    ]