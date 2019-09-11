from django.urls import path
from .views import ListSongView, ListCreateSongsView, SongDetailView

urlpatterns = [
    # path('song/', ListSongView.as_view(), name="song-list")
    path('song/', ListCreateSongsView.as_view(), name="songs-list-create"),
    path('song/<int:pk>/', SongDetailView.as_view(), name="songs-detail"),
]