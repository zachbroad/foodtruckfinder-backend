# Generated by Django 3.0.5 on 2020-09-19 01:58


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trucks', '0009_truckevent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='truckevent',
            options={'ordering': ('start_time',)},
        ),
    ]
