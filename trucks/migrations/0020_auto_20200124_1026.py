# Generated by Django 3.0.2 on 2020-01-24 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trucks', '0019_auto_20200124_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='description',
            field=models.CharField(blank=True, default='Sorry, this truck has no description.', max_length=500, null=True),
        ),
    ]