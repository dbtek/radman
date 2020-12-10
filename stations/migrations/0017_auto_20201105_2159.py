# Generated by Django 3.0.5 on 2020-11-05 18:59

from django.db import migrations, models
import stations.models


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0016_station_site'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Aktif'),
        ),
        migrations.AlterField(
            model_name='player',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Açıklama'),
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(default=stations.models.player_name, max_length=200, verbose_name='İsim'),
        ),
        migrations.AlterField(
            model_name='player',
            name='password',
            field=models.CharField(blank=True, default=stations.models.random_player_password, max_length=500, null=True, verbose_name='Şifre'),
        ),
        migrations.AlterField(
            model_name='player',
            name='slug',
            field=models.CharField(default=stations.models.random_player_slug, max_length=6, unique=True, verbose_name='Slug'),
        ),
    ]