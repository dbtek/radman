from django.contrib import admin

from .models import Station, Mount, Player


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'site')

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Station.objects.all()
        if request.user.groups.filter(name='siteadmin').exists():
            return Station.objects.filter(site=request.user.siteuser.site)


@admin.register(Mount)
class MountAdmin(admin.ModelAdmin):
    readonly_fields = ('mount_point', 'mount_id')

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Mount.objects.all()
        else:
            return Mount.objects.filter(station__site=request.user.siteuser.site)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Player.objects.all()
        else:
            return Player.objects.filter(mount__station__site=request.user.siteuser.site)
