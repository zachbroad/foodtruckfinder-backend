# Generated by Django 2.0.6 on 2019-12-07 01:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trucks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='truck',
            name='owner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='truck',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trucks.Truck'),
        ),
    ]