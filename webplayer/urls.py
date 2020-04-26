from django.urls import path
from webplayer.views import player

urlpatterns = [
    path('play/<uuid:uuid>/', player),
]
