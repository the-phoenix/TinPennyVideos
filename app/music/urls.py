from django.urls import path
from .views import ListSongView, ListCreateSongsView

urlpatterns = [
    # path('song/', ListSongView.as_view(), name="song-list")
    path('song/', ListCreateSongsView.as_view(), name="songs-list-create")
]