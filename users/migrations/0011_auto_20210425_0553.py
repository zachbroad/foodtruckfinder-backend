# Generated by Django 3.1 on 2021-04-25 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trucks', '0017_alter_menuitem_type'),
        ('users', '0010_userreportmodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FavoriteTruck',
            new_name='TruckFavorite',
        ),
    ]