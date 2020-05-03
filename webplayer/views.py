from django.http import Http404
from django.shortcuts import render

from stations.models import Mount
from stations.password import verify_password, hash_password
from webplayer.forms import PlayerForm


def player(request, uuid):
    try:
        m = Mount.objects.get(pk=uuid)
    except Mount.DoesNotExist:
        raise Http404("Kanal bulunamadı")

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
            password = request.POST['password']
            # do password check
            if not verify_password(m.password, password):
                form = PlayerForm(request.POST)
                form.add_error('password', 'Şifre doğru değil.')
                return render(request, 'player_form.html', {'mountId': m.id, 'form': form})
            else:
                request.session['password'] = password
                return render_player()
        else:
            if 'mount_token' in request.session:
                # get mount token from session
                mount_token = request.session['mount_token']
                # do password check
                if not hash_password(m.password) == mount_token:
                    form = PlayerForm(None)
                    form.add_error('password', 'Şifre doğru değil.')
                    return render(request, 'player_form.html', {'mountId': m.id, 'form': form})
                else:
                    return render_player()

            form = PlayerForm(None)
            return render(request, 'player_form.html', {'mountId': m.id, 'form': form})
