from django.contrib.gis.geoip2 import GeoIP2
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from stations.models import Player, VideoPlayer


class ListenerLog(models.Model):
    player = models.ForeignKey(Player, models.CASCADE, verbose_name=_('Player'), null=True, blank=True, )
    video_player = models.ForeignKey(VideoPlayer, models.CASCADE, verbose_name=_('Player'), null=True, blank=True, )
    ip = models.CharField(_('ip'), max_length=100)
    browser = models.TextField(_('Web Browser'), blank=True, null=True)
    organization = models.TextField(_('Organization'), blank=True, null=True)
    name = models.TextField(_('Name - Surname'), blank=True, null=True)
    created = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated at'), auto_now=True)

    def get_browser(self):
        try:
            veri = self.browser.split('(')
            cihaz = veri[1].split(';')[:2]
            tarayici = veri[-1].split()[-1]

            return mark_safe("""
                  Device:<b>{}</b> <br> Browser:<b>{}</b>
                  """.format(' '.join(cihaz).split(')')[0], tarayici))
        except:
            return 'Hata oluştu'

    get_browser.short_description = _('Device & browser info')

    def get_geoip(self):
        g = GeoIP2('geoip')

        try:
            region = g.city(self.ip)
            return mark_safe("""
                              region:<b>{}/{}/{}</b> <br> ip:<b>{}</b>
                              """.format(region['continent_code'], region['country_name'], region['city'], self.ip))
        except:
            pass

        return mark_safe("""
                  region:<b>Bulunamadı</b> <br> ip:<b>{}</b>
                  """.format(self.ip))

    get_geoip.short_description = _('Region info')

    class Meta:
        verbose_name = _('Listener log')
        verbose_name_plural = _('Listener logs')

    def __str__(self):
        return '%s' % (self.name,)
