# Generated by Django 2.2.7 on 2020-01-24 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trucks', '0019_auto_20200124_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='desert',
            field=models.ForeignKey(blank=True, limit_choices_to={'type': 4}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item4', to='trucks.MenuItem'),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='drink',
            field=models.ForeignKey(blank=True, limit_choices_to={'type': 3}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item3', to='trucks.MenuItem'),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='side',
            field=models.ForeignKey(blank=True, limit_choices_to={'type': 2}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item2', to='trucks.MenuItem'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='description',
            field=models.CharField(blank=True, default='Sorry, this truck has no description.', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='entre',
            field=models.ForeignKey(blank=True, limit_choices_to={'type': 1}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item1', to='trucks.MenuItem'),
        ),
    ]