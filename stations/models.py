import uuid
from uuid import uuid4

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

from azuracast import AzuracastClient
from stations.password import hash_password


class Station(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    station_id = models.IntegerField()
    base_url = models.CharField(max_length=500)
    port = models.CharField(max_length=10)
    api_key = models.CharField(max_length=500)
    source_password = models.CharField(max_length=16)
    admin_password = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Mount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    mount_id = models.IntegerField()
    station = models.ForeignKey(to=Station, on_delete=models.PROTECT)
    mount_point = models.UUIDField(null=True, blank=True, unique=True)

    def __str__(self):
        return '%s - %s' % (self.name, self.station.name)


@receiver(pre_save, sender=Mount)
def mount_pre_save(sender, instance, *args, **kwargs):
    if instance._state.adding:
        azuracast = AzuracastClient(instance.station.base_url, instance.station.api_key)
        mount_path = uuid4()

        az_mount = azuracast.add_mount(instance.station.station_id, {
            'name': mount_path,
            'display_name': mount_path,
            'is_visible_on_public_pages': False,
            'is_default': False,
            'is_public': False,
            'enable_autodj': False
        })

        instance.mount_point = mount_path
        instance.mount_id = az_mount['id']


class Player(models.Model):
    name = models.CharField(max_length=200)
    mount = models.ForeignKey(Mount, verbose_name=_('Mount'), on_delete=models.PROTECT)
    slug = models.CharField(null=True, blank=True, unique=True, max_length=6)
    password = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    active = models.BooleanField(verbose_name=_('Active'), default=True)

    def get_stream_url(self):
        return '%s/radio/%s/%s' % (self.mount.station.base_url, self.mount.station.port, self.mount.mount_point)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Player)
def player_pre_save(sender, instance, *args, **kwargs):
    if instance.password:
        instance.password = hash_password(instance.password)
