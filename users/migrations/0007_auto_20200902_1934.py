# Generated by Django 3.0.6 on 2020-09-02 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20200902_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, default='../grubtrucks/assets/grubtruck.png', null=True, upload_to='uploads/user/profile-pictures'),
        ),
    ]
