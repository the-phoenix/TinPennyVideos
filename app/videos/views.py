from rest_framework import generics

from . import models
from . import serializers


class VideoListCreateView(generics.ListCreateAPIView):
    queryset = models.Video.objects.all()
    serializer_class = serializers.VideoSerializer
