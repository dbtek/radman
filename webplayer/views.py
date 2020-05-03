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
            if 'password' in request.session:
                # get password from session
                password = request.session['password']
                # do password check
                if not verify_password(m.password, password):
                    form = PlayerForm(None)
                    form.add_error('password', 'Şifre doğru değil.')
                    return render(request, 'player_form.html', {'mountId': m.id, 'form': form})
                else:
                    return render_player()

            form = PlayerForm(None)
            return render(request, 'player_form.html', {'mountId': m.id, 'form': form})
