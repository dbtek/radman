from django.contrib import admin
from django.contrib.sites.shortcuts import get_current_site

from .models import Station, Mount, Player


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        if request.user.is_superuser:
            return Station.objects.all()
        if request.user.groups.filter(name='siteadmin').exists():
            site = get_current_site(request)
            return Station.objects.filter(site=site)


@admin.register(Mount)
class MountAdmin(admin.ModelAdmin):
    readonly_fields = ('mount_point', 'mount_id')

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Mount.objects.all()
        else:
            site = get_current_site(request)
            return Mount.objects.filter(station__site=site)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Player.objects.all()
        else:
            site = get_current_site(request)
            return Player.objects.filter(mount__station__site=site)
