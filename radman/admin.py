# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from radman.models import SiteUser


class SiteUserInline(admin.StackedInline):
    model = SiteUser
    can_delete = False
    verbose_name_plural = 'user'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (SiteUserInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
