# Generated by Django 2.0.1 on 2018-09-07 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dex', '0002_auto_20180830_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
