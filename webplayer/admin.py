import json
from django.contrib import admin

# Register your models here.
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.utils.translation import ugettext as _

from webplayer.exportxls import export_xls
from webplayer.models import ListenerLog


class PlayerListFilter(admin.RelatedOnlyFieldListFilter):
    def field_choices(self, field, request, model_admin):
        if request.user.is_superuser:
            return super().field_choices(field, request, model_admin)
        return field.get_choices(include_blank=False, limit_choices_to={'mount__station__site': request.user.siteuser.site})


@admin.register(ListenerLog)
class ListenerLogAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'player', 'station', 'created')
    search_fields = ('name', 'organization')
    ordering = ('-updated',)
    actions = [export_xls]

    def station(self, obj):
        return obj.player.mount.station

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return [('player', PlayerListFilter), 'created', 'player__mount__station__site']
        return [('player', PlayerListFilter), 'created']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(player__mount__station__site=request.user.siteuser.site)

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day

        if request.user.is_superuser:
            chart_data = (
                ListenerLog.objects.annotate(date=TruncDay("updated"))
                    .values("date")
                    .annotate(y=Count("id"))
                    .order_by("-date")
            )
        else:
            chart_data = (
                ListenerLog.objects.filter(player__mount__station__site=request.user.siteuser.site).annotate(
                    date=TruncDay("updated"))
                    .values("date")
                    .annotate(y=Count("id"))
                    .order_by("-date")
            )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)
