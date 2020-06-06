from datetime import timedelta

from django.http import Http404
from django.shortcuts import render
from django.utils.timezone import now

from stations.models import Mount
from stations.password import verify_password, hash_password
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


def create_log(request, mount, name, organization):
    timewindow = now() - timedelta(minutes=45)
    ip, browser = get_client_ip(request)
    log = ListenerLog.objects.filter(mount=mount, ip=ip, browser=browser,
                                     name=name, organization=organization,
                                     updated__gt=timewindow).first()
    if not log:
        ListenerLog.objects.create(mount=mount, ip=ip, browser=browser,
                                   organization=organization, name=name)


def player_slim(request, slug):
    try:
        m = Mount.objects.get(slug=slug, active=True)
    except Mount.DoesNotExist:
        raise Http404("Kanal bulunamadı")

    password_sess_key = 'password_%s' % m.id
    name_sess_key = 'name_%s' % m.id
    organization_sess_key = 'organization_%s' % m.id

    if m.password is None:
        return render_player(request, m)
    else:
        if request.POST:
            password = request.POST['password']
            name = request.POST['name']
            organization = request.POST['organization']
            # do password check
            if not verify_password(m.password, password):
                form = PlayerForm(request.POST)
                form.add_error('password', 'Şifre doğru değil.')
                return render(request, 'player_form.html', {'action': '/p/%s/' % m.slug, 'form': form})
            else:
                request.session[password_sess_key] = password
                request.session[name_sess_key] = name
                request.session[organization_sess_key] = organization
                create_log(request, m, name, organization)

                return render_player(request, m)
        else:
            if password_sess_key in request.session and name_sess_key in request.session and organization_sess_key in request.session:
                # get mount token from session
                password = request.session[password_sess_key]
                name = request.session[name_sess_key]
                organization = request.session[organization_sess_key]
                create_log(request, m, name, organization)

                # do password check
                if verify_password(m.password, password):
                    return render_player(request, m)

            form = PlayerForm(None)
            return render(request, 'player_form.html', {'action': '/p/%s/' % m.slug, 'form': form})


def render_player(request, m):
    return render(request, 'player.html', {
        'stationName': m.station.name,
        'mountName': m.name,
        'mountDescription': m.description or '',
        'streamUrl': m.get_stream_url()
    })
