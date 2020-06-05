from django.urls import path
from webplayer.views import player_slim

urlpatterns = [
    path('p/<slug:slug>/', player_slim),
]
