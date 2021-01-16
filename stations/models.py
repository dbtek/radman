import locale
import random
import string
import uuid
from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _


class Station(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    base_url = models.CharField(max_length=500)
    port = models.CharField(max_length=10)
    source_password = models.CharField(max_length=16)
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
    password = models.CharField(verbose_name=_('Password'), max_length=500, null=True, blank=True,
                                default=random_player_password, help_text=_('Leave empty for open access'))
    description = models.TextField(verbose_name=_('Description'), max_length=500, null=True, blank=True)
    active = models.BooleanField(verbose_name=_('Active'), default=True)

    def clean_fields(self, exclude=('mount', 'slug', 'password', 'description', 'active')):
        if self.name == player_name():
            raise ValidationError({'name': _('Please add a descriptive name')}, code='default_name_not_changed',)

    def get_stream_url(self):
        return '%s/%s/%s' % (self.mount.station.base_url, self.mount.station.port, self.mount.mount_point)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id', ]


class VideoPlayer(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=200, default=player_name)
    stream_url = models.CharField(verbose_name=_('Stream URL'), max_length=500)
    slug = models.CharField(verbose_name=_('Slug'), unique=True, max_length=6, default=random_player_slug)
    password = models.CharField(verbose_name=_('Password'), max_length=500, null=True, blank=True,
                                default=random_player_password, help_text=_('Leave empty for open access'))
    description = models.TextField(verbose_name=_('Description'), max_length=500, null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    active = models.BooleanField(verbose_name=_('Active'), default=True)

    def clean_fields(self, exclude=('stream_url', 'slug', 'password', 'description', 'site', 'active')):
        if self.name == player_name():
            raise ValidationError({'name': _('Please add a descriptive name')}, code='default_name_not_changed', )

    def get_stream_url(self):
        return self.stream_url

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id', ]

