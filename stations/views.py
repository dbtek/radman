from uuid import uuid4

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

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

    return render(request, 'mount.html', {'mount': m})


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
            mount_path = uuid4()

            az_mount = azuracast.add_mount(s.station_id, {
              'name': mount_path,
              'display_name': mount_path,
              'is_visible_on_public_pages': False,
              'is_default': False,
              'is_public': False,
              'enable_autodj': False
            })

            m = Mount.objects.create(id=mount_path, name=name, station=s, mount_id=az_mount['id']);

            return HttpResponseRedirect('/mounts/%s' % m.id)

    # get request render form
    else:
        form = MountForm()

    return render(request, 'add_mount.html', {'form': form, 'station': s})