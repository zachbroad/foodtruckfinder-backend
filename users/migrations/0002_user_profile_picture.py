# Generated by Django 3.0.5 on 2020-08-31 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, default='/onthegrub/static/grubtruck.png', null=True, upload_to=''),
        ),
    ]
