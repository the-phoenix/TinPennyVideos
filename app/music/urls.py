from django.urls import path
from .views import LoginView, ListCreateSongsView, SongDetailView

urlpatterns = [
    # path('song/', ListSongView.as_view(), name="song-list")
    path('song/', ListCreateSongsView.as_view(), name="songs-list-create"),
    path('song/<int:pk>/', SongDetailView.as_view(), name="song-detail"),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
]