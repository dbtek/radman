# Generated by Django 3.0.5 on 2020-06-05 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0011_mount_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mount',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]