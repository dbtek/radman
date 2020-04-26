from django.http import Http404
from django.shortcuts import render

from stations.models import Mount


def player(request, uuid):
    try:
        m = Mount.objects.get(pk=uuid)
    except Mount.DoesNotExist:
        raise Http404("Mount does not exist")

    return render(request, 'player.html', {
        'stationName': m.station.name,
        'mountName': m.name,
        'streamUrl': m.get_stream_url()
    })
