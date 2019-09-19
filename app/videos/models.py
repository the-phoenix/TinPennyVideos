from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# Create your models here.
class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=100, blank=False)

    source_url = models.URLField(_('URL to origin video in s3'), blank=False)
    source_thumbnail = models.URLField(_('URL to video thumbnail'), blank=True)
    source_size_in_kb = models.IntegerField(_('video size in kilobytes'), blank=False)

    duration_in_seconds = models.IntegerField(_('duration in seconds'), blank=True)
    stream_url = models.URLField(_('URL to converted stream video'), blank=True)

    user = models.ForeignKey('accounts.User', related_name='videos', on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    # Might need category

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()

        return super(Video, self).save(*args, **kwargs)
