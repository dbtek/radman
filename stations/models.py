import uuid
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

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
    slug = models.CharField(null=True, blank=True, unique=True, max_length=6)
    password = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)

    def get_stream_url(self):
        return '%s/radio/%s/%s' % (self.station.base_url, self.station.port, self.id)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Mount)
def mount_pre_save(sender, instance, *args, **kwargs):
    if instance.password:
        instance.password = hash_password(instance.password)
