import os
from urllib.parse import urlparse, urlunparse
from uuid import uuid4

from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from furl import furl

from azuracast import AzuracastClient
from stations.forms import MountForm
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


def add_mount(request, uuid):
    try:
        s = Station.objects.get(pk=uuid)
    except Mount.DoesNotExist:
        raise Http404("Station does not exist")

    # POST request, process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MountForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            azuracast = AzuracastClient(s.base_url, s.api_key)
            name = request.POST['name']
            password = request.POST['password']
            mount_path = uuid4()

            az_mount = azuracast.add_mount(s.station_id, {
                'name': mount_path,
                'display_name': mount_path,
                'is_visible_on_public_pages': False,
                'is_default': False,
                'is_public': False,
                'enable_autodj': False
            })

            m = Mount.objects.create(id=mount_path, name=name, password=password, station=s, mount_id=az_mount['id']);

            return HttpResponseRedirect('/mounts/%s' % m.id)

    # get request render form
    else:
        form = MountForm()

    return render(request, 'add_mount.html', {'form': form, 'station': s})


def edit_mount(request, uuid):
    try:
        m = Mount.objects.get(pk=uuid)
    except Mount.DoesNotExist:
        raise Http404("Mount does not exist")

    # POST request, process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MountForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            m.name = request.POST['name']
            m.password = request.POST['password']
            m.save()

            return HttpResponseRedirect('/mounts/%s' % m.id)

    # get request render form
    else:
        form = MountForm({"name": m.name})

    return render(request, 'edit_mount.html', {'form': form, 'mount': m})
