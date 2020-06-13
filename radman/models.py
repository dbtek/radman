from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models


class SiteUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return self.site.name
