


from django.db import migrations, models

from trucks.models import Review


class Migration(migrations.Migration):
    dependencies = [
        ('trucks', '0004_auto_20200227_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='review',
            field=models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes', unique=False),
        )
    ]