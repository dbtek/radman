from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

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


def make_active(modeladmin, request, queryset):
    queryset.update(active=True)


make_active.short_description = _('Mark selected players active')


def make_inactive(modeladmin, request, queryset):
    queryset.update(active=False)


make_inactive.short_description = _('Mark selected players inactive')


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'play_url', 'play_widget')
    actions = [make_active, make_inactive]

    def play_widget(self, obj):
        return mark_safe('<audio controls src="%s/%s">%s</audio>' % (
            obj.mount.station.base_url,
            obj.mount.mount_point,
            '<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24">'
            '<path d="M0 0h24v24H0z" fill="none"/>'
            '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/>'
            '</svg>'
        ))

    play_widget.short_description = _('Play')

    def play_url(self, obj):
        return mark_safe(
            '<a href="{base_uri}p/{slug}">{base_uri}p/{slug}</a>'.format(base_uri=self.base_uri, slug=obj.slug)
        )

    play_url.short_description = _('Play URL')

    def get_queryset(self, request):
        self.base_uri = request.build_absolute_uri('/')
        if request.user.is_superuser:
            return Player.objects.all()
        else:
            return Player.objects.filter(mount__station__site=request.user.siteuser.site)
