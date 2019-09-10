from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
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
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, ]
    search_fields = ['artist']
    filterset_fields = ['artist']