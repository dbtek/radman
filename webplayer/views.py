from datetime import timedelta

from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import render
from django.utils.timezone import now

from stations.models import Mount, Player
from webplayer.forms import PlayerForm
from webplayer.models import ListenerLog


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    browser = request.META['HTTP_USER_AGENT']
    return ip, browser


def create_log(request, player, name, organization):
    timewindow = now() - timedelta(minutes=45)
    ip, browser = get_client_ip(request)
    log = ListenerLog.objects.filter(player=player, ip=ip, browser=browser,
                                     name=name, organization=organization,
                                     updated__gt=timewindow).first()
    if not log:
        ListenerLog.objects.create(player=player, ip=ip, browser=browser,
                                   organization=organization, name=name)


def player_slim(request, slug):
    try:
        p = Player.objects.get(slug=slug, active=True, mount__station__site=get_current_site(request))
    except Player.DoesNotExist:
        raise Http404("Kanal bulunamadı")

    password_sess_key = 'password_%s' % p.id
    name_sess_key = 'name_%s' % p.id
    organization_sess_key = 'organization_%s' % p.id

    if p.password is None:
        return render_player(request, p)
    else:
        if request.POST:
            password = request.POST['password']
            name = request.POST['name']
            organization = request.POST['organization']
            # do password check
            if not p.password == password:
                form = PlayerForm(request.POST)
                form.add_error('password', 'Şifre doğru değil.')
                return render(request, 'player_form.html', {'action': '/p/%s/' % p.slug, 'form': form})
            else:
                request.session[password_sess_key] = password
                request.session[name_sess_key] = name
                request.session[organization_sess_key] = organization
                create_log(request, p, name, organization)

                return render_player(request, p)
        else:
            if password_sess_key in request.session and name_sess_key in request.session and organization_sess_key in request.session:
                # get mount token from session
                password = request.session[password_sess_key]
                name = request.session[name_sess_key]
                organization = request.session[organization_sess_key]
                create_log(request, p, name, organization)

                # do password check
                if p.password == password:
                    return render_player(request, p)

            form = PlayerForm(None)
            return render(request, 'player_form.html', {'action': '/p/%s/' % p.slug, 'form': form})


def render_player(request, p):
    return render(request, 'player.html', {
        'stationName': p.mount.station.name,
        'playerName': p.name,
        'mountName': p.mount.name,
        'playerDescription': p.description or '',
        'streamUrl': p.get_stream_url()
    })
