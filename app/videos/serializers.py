from rest_framework import serializers
from . import models


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    # user = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True, lookup_field="id", lookup_url_kwarg="pk")
    publisher = serializers.ReadOnlyField(source='publisher.id')

    class Meta:
        model = models.Video
        fields = ('id', 'title', 'source_url', 'source_thumbnail', 'source_size_in_kb',
                  'stream_url', 'duration_in_seconds', 'created', 'modified',
                  'publisher', 'is_private')
        read_only_fields = ('id', 'source_thumbnail', 'source_size_in_kb',
                            'stream_url', 'publisher',
                            'duration_in_seconds', 'created', 'modified')
