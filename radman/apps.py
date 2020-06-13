from django.contrib.admin.apps import AdminConfig


class RadmanAdminConfig(AdminConfig):
    default_site = 'radman.admin.RadmanAdminSite'
