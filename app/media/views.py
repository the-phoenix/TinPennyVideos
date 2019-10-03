from rest_framework import permissions, viewsets

from .models import Video, Category, Stream
from .serializers import VideoSerializer, CategorySerializer, StreamSerializer
from .permissions import IsOwnerOrReadonly


class VideoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    # queryset = Video.objects.exclude(is_public=False)
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadonly]

    def get_queryset(self):
        title = self.request.query_params.get('title', '').lower()

        queryset = Video.objects\
            .exclude(is_public=False)\
            .filter(title__icontains=title)

        return queryset

    def perform_create(self, serializer):
        source_path = self.request.data.get('source_path')
        publisher = self.requeset.user
        if source_path is not None:
            return serializer.save(source=source_path, publisher=publisher)

        return serializer.save(publisher=publisher)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class StreamViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]