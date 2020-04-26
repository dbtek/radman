from django.urls import path

from stations.views import add_mount, station, mount

urlpatterns = [
    path('stations/<uuid:uuid>/', station),
    path('stations/<uuid:uuid>/add-mount/', add_mount),
    path('mounts/<uuid:uuid>/', mount),
]
