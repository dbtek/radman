import locale
from datetime import datetime
import string
import uuid
import random
from uuid import uuid4
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
from azuracast import AzuracastClient


class Station(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    station_id = models.IntegerField()
    base_url = models.CharField(max_length=500)
    port = models.CharField(max_length=10)
    api_key = models.CharField(max_length=500)
    source_password = models.CharField(max_length=16)
    admin_password = models.CharField(max_length=16)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

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


def random_player_slug():
    letters = string.ascii_lowercase
    length = 6
    return ''.join(random.choice(letters) for i in range(length))


def random_player_password():
    return random.randint(1000, 9999)


def player_name():
    locale.setlocale(locale.LC_TIME, "tr_TR")
    return datetime.now().strftime("%d %B")


class Player(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=200, default=player_name)
    mount = models.ForeignKey(Mount, verbose_name=_('Mount'), on_delete=models.PROTECT)
    slug = models.CharField(verbose_name=_('Slug'), unique=True, max_length=6, default=random_player_slug)
    password = models.CharField(verbose_name=_('Password'), max_length=500, null=True, blank=True, default=random_player_password)
    description = models.TextField(verbose_name=_('Description'), max_length=500, null=True, blank=True)
    active = models.BooleanField(verbose_name=_('Active'), default=True)

    def get_stream_url(self):
        return '%s/%s/%s' % (self.mount.station.base_url, self.mount.station.port, self.mount.mount_point)

    def __str__(self):
        return self.name
