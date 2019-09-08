from rest_framework import generics
# from django.shortcuts import render
from .models import Song
from .serializers import SongSerializer


# Create your views here.

class ListSongView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer
