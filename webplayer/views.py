from datetime import timedelta

from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import render
from django.utils.timezone import now

from stations.models import Mount, Player, VideoPlayer
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


def create_video_log(request, player, name, organization):
    timewindow = now() - timedelta(minutes=45)
    ip, browser = get_client_ip(request)
    log = ListenerLog.objects.filter(video_player=player, ip=ip, browser=browser,
                                     name=name, organization=organization,
                                     updated__gt=timewindow).first()
    if not log:
        ListenerLog.objects.create(video_player=player, ip=ip, browser=browser,
                                   organization=organization, name=name)


def player_slim(request, slug):
    is_video = False
    try:
        p = Player.objects.get(slug=slug, active=True, mount__station__site=get_current_site(request))
    except Player.DoesNotExist:
        is_video = True
        p = VideoPlayer.objects.get(slug=slug, active=True, site=get_current_site(request))
    except VideoPlayer.DoesNotExist:
        raise Http404("Kanal bulunamadı")

    password_sess_key = 'password_%s' % p.id
    name_sess_key = 'name_%s' % p.id
    organization_sess_key = 'organization_%s' % p.id

    if p.password is None:
        return render_player(request, p, is_video)
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
                if is_video:
                    create_video_log(request, p, name, organization)
                else:
                    create_log(request, p, name, organization)

                return render_player(request, p, is_video)
        else:
            if password_sess_key in request.session and name_sess_key in request.session and organization_sess_key in request.session:
                # get mount token from session
                password = request.session[password_sess_key]
                name = request.session[name_sess_key]
                organization = request.session[organization_sess_key]
                if is_video:
                    create_video_log(request, p, name, organization)
                else:
                    create_log(request, p, name, organization)

                # do password check
                if p.password == password:
                    return render_player(request, p, is_video)

            form = PlayerForm(None)
            return render(request, 'player_form.html', {'action': '/p/%s/' % p.slug, 'form': form})


def render_player(request, p, is_video):
    if is_video:
        return render(request, 'videoplayer.html', {
            'playerName': p.name,
            'playerDescription': (p.description or '').replace('\n', '<br/>'),
            'streamUrl': p.get_stream_url()
        })
    else:
        return render(request, 'player.html', {
            'stationName': p.mount.station.name,
            'playerName': p.name,
            'mountName': p.mount.name,
            'playerDescription': (p.description or '').replace('\n', '<br/>'),
            'streamUrl': p.get_stream_url()
        })
