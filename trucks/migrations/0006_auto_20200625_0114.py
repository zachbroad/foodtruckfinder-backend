# Generated by Django 3.0.6 on 2020-06-25 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trucks', '0005_auto_20200623_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='image',
            field=models.ImageField(blank=True, default='../media/assets/truck_logo_placeholder.png', upload_to='uploads/trucks/menu-items'),
        ),
    ]