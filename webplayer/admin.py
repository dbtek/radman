import json
from abc import ABC
from datetime import datetime, timedelta

from django.contrib import admin

# Register your models here.
from django.contrib.sites.models import Site
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Q
from django.db.models.functions import TruncDay
from django.utils.translation import ugettext as _

from webplayer.exportxls import export_xls
from webplayer.models import ListenerLog


class PlayerListFilter(admin.RelatedOnlyFieldListFilter):
    def field_choices(self, field, request, model_admin):
        if request.user.is_superuser:
            return super().field_choices(field, request, model_admin)
        return field.get_choices(include_blank=False,
                                 limit_choices_to={
                                     'mount__station__site': request.user.siteuser.site,
                                 })[:10]


class VideoPlayerListFilter(admin.RelatedOnlyFieldListFilter):
    def field_choices(self, field, request, model_admin):
        if request.user.is_superuser:
            return super().field_choices(field, request, model_admin)
        return field.get_choices(include_blank=False,
                                 limit_choices_to={
                                     'site': request.user.siteuser.site
                                 })[:10]


class SiteListFilter(admin.SimpleListFilter, ABC):
    title = _('Site')
    parameter_name = 'site'

    def queryset(self, request, queryset):
        return queryset.filter(Q(player__mount__station__site__id=self.value()) | Q(
            video_player__site__id=self.value()))

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            sites = Site.objects.all()
        else:
            sites = (request.user.siteuser.site,)
        return map(lambda x: (x.id, x.name), sites)


@admin.register(ListenerLog)
class ListenerLogAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'player', 'video_player', 'get_site', 'created')
    search_fields = ('name', 'organization')
    ordering = ('-id',)
    actions = [export_xls]

    def get_site(self, obj):
        if obj.player is not None:
            return obj.player.mount.station.site
        if obj.video_player is not None:
            return obj.video_player.site

    get_site.short_description = _('Site')

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return [SiteListFilter, ('player', PlayerListFilter), ('video_player', VideoPlayerListFilter), 'created',]
        return [('player', PlayerListFilter), ('video_player', VideoPlayerListFilter), 'created']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(player__mount__station__site=request.user.siteuser.site) | Q(
            video_player__site=request.user.siteuser.site))

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        begin_date = datetime.now() - timedelta(days=8)

        chart_data = (
            self.get_queryset(request)
                .filter(updated__gt=begin_date)
                .annotate(date=TruncDay("updated"))
                .values("date")
                .annotate(y=Count("id"))
                .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)
