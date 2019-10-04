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
        title = self.request.query_params.get('title', None)
        queryset = Video.objects.exclude(is_public=False)

        if title is not None:
            queryset = queryset.filter(title__icontains=title.lower())

        return queryset

    def perform_create(self, serializer):
        source_path = self.request.data.get('source_path', None)
        publisher = self.request.user
        if source_path is not None:
            return serializer.save(source=source_path, publisher=publisher)

        return serializer.save(publisher=publisher)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list`, `retrieve`, actions.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class StreamViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list`, `retrieve`, actions.
    """
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    permission_classes = [permissions.AllowAny]