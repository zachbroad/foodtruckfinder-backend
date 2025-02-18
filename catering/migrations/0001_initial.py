# Generated by Django 3.0.6 on 2020-07-25 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CaterRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254)),
                ('details', models.TextField(max_length=10000)),
                ('when', models.DateTimeField()),
                ('duration', models.FloatField()),
            ],
            options={
                'ordering': ('-when',),
            },
        ),
    ]
