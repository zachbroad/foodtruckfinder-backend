# Generated by Django 3.0.5 on 2020-09-23 14:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trucks', '0010_auto_20200918_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='truck',
            name='description',
            field=models.TextField(blank=True, default='Sorry, this truck has no description.', max_length=3000),
        ),
        migrations.AlterField(
            model_name='truck',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]