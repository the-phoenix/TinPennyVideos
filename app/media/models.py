from uuid import uuid4
from django import forms
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


from .validators import s3_path_validator
from .tasks_without_model import remove_video_files, remove_stream_files
from .utils import path_and_rename, s3_to_http_schema


class S3PathField(models.CharField):
    description = _("S3 Path")
    # '''URL field that accepts URLs that start with s3:// only.'''
    default_validators = [s3_path_validator]

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 200
        kwargs['help_text'] = "Format: s3://{bucket name}/{file name}"
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get("max_length") == 200:
            del kwargs['max_length']
        if kwargs.get("help_text") == "Format: s3://{bucket name}/{file name}":
            del kwargs['help_text']
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        # As with CharField, this will cause URL validation to be performed
        # twice.
        return super().formfield(**{
            'form_class': forms.URLField,
            **kwargs,
        })


# Create your models here.

class Category(models.Model):
    name = models.CharField(_('Name of category'), max_length=100, blank=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Video(models.Model):
    NOT_STARTED = 'not_started'
    STARTED = 'started'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'

    MEDIA_CONVERT_STATUSES = [
        (NOT_STARTED, _('Not started')),
        (STARTED, _('Started')),
        (SUCCEEDED, _('Succeeded')),
        (FAILED, _('Failed')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=100, blank=False)

    # Expect client do S3 upload with unique name
    # origin = models.FileField(blank=True, unique=True, storage=settings.FILE_STORAGE_FOR_ORIGIN_VIDEO)
    origin = models.FileField(blank=False, upload_to=path_and_rename,
                              validators=[FileExtensionValidator(allowed_extensions=settings.ACCEPTABLE_VIDEO_FILE_EXTENSIONS)])
    origin_size_in_kb = models.IntegerField(_('video size in kilobytes'), blank=True, null=True)

    poster_thumbnail = S3PathField(_('Path to poster frame for video'), blank=True)
    duration_in_ms = models.IntegerField(_('duration in milli seconds'), blank=True, null=True)

    publisher = models.ForeignKey('accounts.User', related_name='videos', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='videos', on_delete=models.DO_NOTHING)
    is_public = models.BooleanField(_('Is public?'), default=True)
    mc_status = models.CharField(_('Media convert status'), choices=MEDIA_CONVERT_STATUSES, default=NOT_STARTED,
                                 help_text=_('Updated by celery jobs. Do not update manually'), blank=False, max_length=50)
    failure_reason = models.TextField(_('Failure reason of media convert'), blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('modified',)

    def __str__(self):
        return self.title

    @property
    def poster_thumbnail_distributed(self):
        if self.poster_thumbnail is None:
            return None

        http_urls = s3_to_http_schema(self.poster_thumbnail)

        return http_urls["distributed"]

    def save(self, *args, **kwargs):
        # Once video's uploaded S3, it triggers convert automatically
        if self.id is None:
            self.mc_status = Video.STARTED

        return super(Video, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.origin is not None:
            remove_video_files.delay(self.origin.name, self.poster_thumbnail)

        if self.streams is not None:
            for stream in self.streams.all():
                stream.delete()

        return super(Video, self).delete(*args, **kwargs)


class Stream(models.Model):
    origin = models.ForeignKey(Video, related_name='streams', on_delete=models.CASCADE)
    path = S3PathField("Full S3 Path to converted video stream", blank=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def path_distributed(self):
        if self.path is None:
            return None

        http_urls = s3_to_http_schema(self.path)

        return http_urls["distributed"]

    def __str__(self):
        return self.path

    def delete(self, *args, **kwargs):
        remove_stream_files.delay(self.path)

        return super(Stream, self).delete(*args, **kwargs)