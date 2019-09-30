from rest_framework import serializers
from django.conf import settings
from . import models
from .utils import is_existing_in_bucket


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    # user = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True, lookup_field="id", lookup_url_kwarg="pk")
    publisher = serializers.ReadOnlyField(source='publisher.id')

    class Meta:
        model = models.Video
        fields = ('id', 'title', 'origin', 'origin_size_in_kb', 'category', 'poster_thumbnail',
                  'duration_in_ms', 'mc_status', 'streams', 'failure_reason',
                  'publisher', 'is_private', 'created', 'modified',)
        read_only_fields = ('id', 'poster_thumbnail', 'publisher',
                            'duration_in_ms', 'created', 'modified')

    def is_valid(self, *args, **kwargs):
        origin_path = self.initial_data.get('origin_path')
        if origin_path is not None:
            if not is_existing_in_bucket(origin_path, settings.AWS_STORAGE_BUCKET_NAME):
                raise serializers.ValidationError("Not existing in S3 bucket!")

        return super(VideoSerializer, self).is_valid(*args, **kwargs)
