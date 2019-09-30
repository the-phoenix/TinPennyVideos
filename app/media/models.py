from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
# from django.utils import timezone
from django.conf import settings
from .validators import s3_path_validator


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


# Create your models here.

class Category(models.Model):
    name = models.CharField(_('Category of video'), max_length=100, blank=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

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
    origin = models.FileField(blank=False)
            # models.CharField(_('Key to origin video in s3 bucket'), max_length=200, blank=False, unique=True)
    origin_size_in_kb = models.IntegerField(_('video size in kilobytes'), blank=True, null=True)

    poster_thumbnail = S3PathField(_('Path to poster frame for video'), blank=True)
    duration_in_ms = models.IntegerField(_('duration in milli seconds'), blank=True, null=True)
    convert_failure_reason = models.TextField(_('Reason for media convert failure'), blank=True)

    publisher = models.ForeignKey('accounts.User', related_name='videos', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='videos', on_delete=models.DO_NOTHING)
    is_private = models.BooleanField(_('is private?'), default=False)
    mc_status = models.CharField(choices=MEDIA_CONVERT_STATUSES, default=NOT_STARTED, blank=False, max_length=50)
    failure_reason = models.TextField(_('Failure reason of media convert'), blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('modified',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Once video's uploaded S3, it triggers convert automatically
        if self.id is None:
            self.mc_status = Video.STARTED

        return super(Video, self).save(*args, **kwargs)


class Stream(models.Model):
    origin = models.ForeignKey(Video, related_name='streams', on_delete=models.CASCADE)
    path = S3PathField("Full S3 Path to converted video stream", blank=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.path

    #TODO: When its deleted, try to remove all related files in s3