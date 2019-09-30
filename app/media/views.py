from rest_framework import permissions, viewsets

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

    def perform_create(self, serializer):
        source_path = self.request.data.get('source_path')
        publisher = self.requeset.user
        if source_path is not None:
            return serializer.save(source=source_path, publisher=publisher)

        return serializer.save(publisher=publisher)