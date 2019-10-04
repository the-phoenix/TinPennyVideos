from rest_framework import serializers
from django.conf import settings
from . import models
from .utils import is_existing_in_bucket


class VideoSerializer(serializers.HyperlinkedModelSerializer):

    publisher = serializers.ReadOnlyField(source='publisher.id')
    category_name = serializers.ReadOnlyField(source='category.name')
    # category_name = serializers.RelatedField(source='category', read_only=True)
    streams = serializers.SlugRelatedField(many=True, read_only=True, slug_field='path_distributed')

    class Meta:
        model = models.Video
        fields = ('id', 'title', 'origin', 'origin_size_in_kb', 'category',
                  'poster_thumbnail_distributed', 'category_name',
                  'duration_in_ms', 'mc_status', 'streams', 'failure_reason',
                  'publisher', 'is_public', 'created', 'modified',)

        read_only_fields = ('id', 'publisher', 'mc_status', 'failure_reason',
                            'duration_in_ms', 'created', 'modified')
        extra_kwargs = {
            'category': {'write_only': True},
            'origin': {'write_only': True},
        }

    def is_valid(self, *args, **kwargs):
        origin_path = self.initial_data.get('origin_path')
        if origin_path is not None:
            if not is_existing_in_bucket(bucket=settings.AWS_STORAGE_BUCKET_NAME, key=origin_path):
                raise serializers.ValidationError("Not existing in S3 bucket!")

        return super(VideoSerializer, self).is_valid(*args, **kwargs)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class StreamSerializer(serializers.ModelSerializer):
    path_distributed = serializers.ReadOnlyField()

    class Meta:
        model = models.Stream
        fields = '__all__'
