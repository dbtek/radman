# Generated by Django 3.0.5 on 2020-06-06 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0012_auto_20200605_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='mount',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
    ]
