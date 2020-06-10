from django.urls import path

from stations import views

urlpatterns = [
    path('stations/<uuid:uuid>/', views.station),
    path('mounts/<uuid:uuid>/', views.mount),
    path('mounts/<uuid:uuid>/butt/', views.download_config),
]
