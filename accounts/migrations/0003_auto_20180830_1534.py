# Generated by Django 2.0.1 on 2018-08-30 15:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dex', '0002_auto_20180830_1534'),
        ('accounts', '0002_auto_20180828_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activistorgs',
            name='activist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='activistorgs',
            unique_together={('activist', 'organization')},
        ),
        migrations.AlterUniqueTogether(
            name='organizer',
            unique_together={('organizer', 'organization')},
        ),
    ]
