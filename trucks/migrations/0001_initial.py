
# Generated by Django 2.2.7 on 2019-11-10 00:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/trucks/profile-pictures')),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('price', models.FloatField(max_length=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/trucks/menu-items')),
                ('truck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trucks.Truck')),
            ],
        ),
    ]
