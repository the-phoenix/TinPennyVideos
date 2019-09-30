import datetime

from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core import validators

s3_path_validator = validators.RegexValidator(
    regex='^s3://([^/]+)/(.*?([^/]+)/?)$',
    message='Enter a valid S3 Path',
)


class S3PathField(models.CharField):
    description = _("S3 Path")
    # '''URL field that accepts URLs that start with ssh:// only.'''
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
    source_path = S3PathField(_('Path to origin video in s3'),
                              blank=False, unique=True)
    source_size_in_kb = models.IntegerField(_('video size in kilobytes'), blank=True, null=True)

    poster_thumbnail = S3PathField(_('Path to poster frame for video'), blank=True)

    duration_in_ms = models.IntegerField(_('duration in milli seconds'), blank=True, null=True)
    stream_path = models.CharField(_('Path to converted stream video'), max_length=200, blank=True, null=True)

    convert_failure_reason = models.TextField(_('Reason for media convert failure'), null=True)

    publisher = models.ForeignKey('accounts.User', related_name='videos', on_delete=models.CASCADE)
    is_private = models.BooleanField('is private?', default=False)
    mc_status = models.CharField(choices=MEDIA_CONVERT_STATUSES, default=NOT_STARTED, blank=False)
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField()

    # Might need category

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Once video's uploaded S3, it triggers convert automatically
        if self.id is not None:
            self.mc_status = Video.STARTED

        self.modified = timezone.now()

        return super(Video, self).save(*args, **kwargs)
