import json
from django.contrib import admin

# Register your models here.
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay

from webplayer.exportxls import export_xls
from webplayer.models import ListenerLog


@admin.register(ListenerLog)
class ListenerLogAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'player', 'created')
    search_fields = ('name', 'organization')
    ordering = ('-updated',)
    list_filter = ('player', 'created')
    actions = [export_xls]

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
                ListenerLog.objects.filter(link__user=request.user).annotate(date=TruncDay("updated"))
                    .values("date")
                    .annotate(y=Count("id"))
                    .order_by("-date")
            )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)

