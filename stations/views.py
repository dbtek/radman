import os
from urllib.parse import urlparse, urlunparse
from uuid import uuid4

from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from furl import furl

from azuracast import AzuracastClient
from stations.models import Mount, Station


def station(request, uuid):
    try:
        s = Station.objects.get(pk=uuid)
        ms = Mount.objects.all().filter(station=s)
    except Mount.DoesNotExist:
        raise Http404("Station does not exist")

    return render(request, 'station.html', {'station': s, 'mounts': ms})


def mount(request, uuid):
    try:
        m = Mount.objects.get(pk=uuid)
    except Mount.DoesNotExist:
        raise Http404("Mount does not exist")

    hurl = urlparse(m.station.base_url)

    surl = furl(m.station.base_url)
    surl.username = 'source'
    surl.password = m.station.source_password
    surl.port = m.station.port
    surl.path = m.id.__str__()

    return render(request, 'mount.html', {'mount': m, 'host': hurl.netloc, 'coolmic_url': surl})


def download_config(request, uuid):
    try:
        m = Mount.objects.get(pk=uuid)
    except Mount.DoesNotExist:
        raise Http404("Mount does not exist")

    config = """
#This is a configuration file for butt (broadcast using this tool)
[main]
server = {stationName}
srv_ent = {stationName}
gain = 1.000000
num_of_srv = 1
icy = {mountName}
icy_ent = {mountName}
num_of_icy = 1

[{stationName}]
address = {host}
port = {port}
password = {password}
type = 1
tls = 1
mount = {mount}
usr = source

[{mountName}]
pub = 0
description = {mountName}
genre = misc
    """.format(stationName=m.station.name, mountName=m.name, host=urlparse(m.station.base_url).netloc,
               port=m.station.port, mount=m.id, password=m.station.source_password)

    response = HttpResponse(config, content_type="application/text")
    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(m.name + '.txt')
    return response
