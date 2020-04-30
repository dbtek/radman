from django.http import Http404
from django.shortcuts import render

from stations.models import Mount
from stations.password import verify_password
from webplayer.forms import PlayerForm


def player(request, uuid):
    try:
        m = Mount.objects.get(pk=uuid)
    except Mount.DoesNotExist:
        raise Http404("Mount does not exist")

    def render_player():
        return render(request, 'player.html', {
            'stationName': m.station.name,
            'mountName': m.name,
            'streamUrl': m.get_stream_url()
        })

    if m.password is None:
        return render_player()
    else:
        if request.POST:
            # do password check
            validpass = verify_password(m.password, request.POST['password'])
            if not validpass:
                form = PlayerForm(request.POST)
                form.add_error('password', 'Şifre doğru değil.')
                return render(request, 'player_form.html', {'mountId': m.id, 'form': form})
            else:
                return render_player()
        else:
            form = PlayerForm(None)
            return render(request, 'player_form.html', {'mountId': m.id, 'form': form})
