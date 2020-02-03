# Generated by Django 2.2.7 on 2020-01-23 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trucks', '0014_auto_20200123_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='entre',
            field=models.ForeignKey(default=None, limit_choices_to={'type': 1}, on_delete=django.db.models.deletion.CASCADE, to='trucks.MenuItem'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='type',
            field=models.IntegerField(choices=[(1, 'Entre'), (2, 'Side'), (3, 'Drink'), (4, 'Desert')]),
        ),
        migrations.DeleteModel(
            name='MenuItemCombo',
        ),
    ]