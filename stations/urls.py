from django.urls import path

from stations import views

urlpatterns = [
    path('stations/<uuid:uuid>/', views.station),
    path('stations/<uuid:uuid>/add-mount/', views.add_mount),
    path('mounts/<uuid:uuid>/', views.mount),
]
