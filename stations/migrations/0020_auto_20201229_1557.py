# Generated by Django 3.0.5 on 2020-12-29 12:57

from django.db import migrations, models
import django.db.models.deletion
import stations.models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('stations', '0019_remove_station_admin_password'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='player',
            name='password',
            field=models.CharField(blank=True, default=stations.models.random_player_password, help_text='Leave empty for open access', max_length=500, null=True, verbose_name='Şifre'),
        ),
        migrations.CreateModel(
            name='VideoPlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=stations.models.player_name, max_length=200, verbose_name='İsim')),
                ('stream_url', models.CharField(max_length=500, verbose_name='Stream URL')),
                ('slug', models.CharField(default=stations.models.random_player_slug, max_length=6, unique=True, verbose_name='Slug')),
                ('password', models.CharField(blank=True, default=stations.models.random_player_password, help_text='Leave empty for open access', max_length=500, null=True, verbose_name='Şifre')),
                ('description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Açıklama')),
                ('active', models.BooleanField(default=True, verbose_name='Aktif')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
