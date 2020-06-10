from django.contrib import admin

from .models import Station, Mount, Player

admin.site.register(Station)
admin.site.register(Player)


@admin.register(Mount)
class MountAdmin(admin.ModelAdmin):
    readonly_fields = ('mount_point', 'mount_id')