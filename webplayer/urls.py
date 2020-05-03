from django.urls import path
from webplayer.views import player, player_slim

urlpatterns = [
    path('play/<uuid:uuid>/', player),
    path('p/<slug:slug>/', player_slim),
]
