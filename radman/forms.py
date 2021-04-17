from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError


class RadmanAdminLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        site = get_current_site(self.request)
        if not user.is_superuser and user.siteuser.site.domain != site.domain:
            raise ValidationError('You are not allowed to login on this site.', code='inactive')
