from rest_framework import generics, permissions, renderers, viewsets

from .models import Video
from .serializers import VideoSerializer
from .permissions import IsOwnerOrReadonly


class VideoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Video.objects.exclude(is_private=True)
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadonly]

    # def list(self, request, *args, **kwargs):
    #     super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(publisher=self.request.user)
