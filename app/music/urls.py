from django.urls import path
from .views import ListSongView

urlpatterns = [
    path('song/', ListSongView.as_view(), name="song-list")
]