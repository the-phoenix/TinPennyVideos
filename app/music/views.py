
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

# class SongDetailView(generics.RetrieveUpdateDestroyAPIView):
class SongDetailView(generics.RetrieveAPIView):
    """
    GET songs/:id/
    PUT songs/:id/
    DELETE songs/:id/
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            return Response(SongSerializer(a_song).data)
        except Song.DoesNotExist:
            return Response(
                data={
                    "message": "Song with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    # @validate_request_data
    # def put(self, request, *args, **kwargs):
    #     try:
    #         a_song = self.queryset.get(pk=kwargs["pk"])
    #         serializer = SongSerializer()
    #         up
