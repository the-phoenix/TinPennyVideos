
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.views import status


# from django.shortcuts import render

from .decorators import validate_request_data
from .models import Song
from .serializers import SongSerializer


# Create your views here.
# Not being used
class ListSongView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, ]
    search_fields = ['artist']
    filterset_fields = ['artist']


class ListCreateSongsView(generics.ListCreateAPIView):
    """
    GET songs/
    POST
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    @validate_request_data
    def post(self, request, *args, **kwargs):
        a_song = Song.objects.create(
            title=request.data["title"],
            artist=request.data["artist"]
        )

        return Response(
            data=SongSerializer(a_song).data,
            status=status.HTTP_201_CREATED
        )
