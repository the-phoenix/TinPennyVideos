import datetime

from django.contrib import admin
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import AdminURLFieldWidget
from django.utils.html import smart_urlquote
from django.utils.translation import gettext_lazy as _
from urllib.parse import urlparse

from .models import Video, Category, Stream, S3PathField
from .utils import td_format
from .validators import s3_path_validator


class AdminS3PathFieldWidget(AdminURLFieldWidget):
    template_name = 'admin/widgets/s3-path.html'

    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'vS3PathField', **(attrs or {})}, validator_class=lambda : s3_path_validator)

    def get_context(self, name, value, attrs):
        try:
            self.validator(value if value else '')
            url_valid = True
        except ValidationError:
            url_valid = False
        context = super().get_context(name, value, attrs)
        context['current_label'] = _('Currently:')
        context['change_label'] = _('Change:')
        context['url_valid'] = url_valid

        if url_valid is True:
            parsed = urlparse(value)
            bucket = parsed.netloc
            key = parsed.path.strip('/')

            if bucket == settings.AWS_STREAM_STORAGE_BUCKET_NAME:
                context['distributed_label'] = _('Distributed:')
                context['distributed_value'] = smart_urlquote("https://{0}/{1}".format(settings.CLOUDFRONT_DNS_NAME, key))

            href_to_s3_console = "https://s3.console.aws.amazon.com/s3/object/{bucket}/{key}?tab=overview".format(bucket=bucket, key=key)
            context['widget']['href'] = smart_urlquote(href_to_s3_console)

        return context


class StreamAdminInline(admin.TabularInline):
    formfield_overrides = {
        S3PathField: {'widget': AdminS3PathFieldWidget},
    }
    model = Stream

# Register your models here.
@admin.register(Video)
class VideosAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'origin', 'mc_status', 'duration', 'is_public', 'modified')
    list_display_links = ('id', 'title', )
    inlines = (StreamAdminInline,)
    formfield_overrides = {
        S3PathField: {'widget': AdminS3PathFieldWidget},
    }

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return "origin", "origin_size_in_kb",
        else:
            return ()

    def duration(self, obj):
        if obj.duration_in_ms is None:
            return None

        return td_format(datetime.timedelta(milliseconds=obj.duration_in_ms))

    duration.admin_order_field = 'duration_in_ms'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_video_count', 'modified')
    fields = ('name', 'category_video_count', 'created', 'modified',)
    readonly_fields = ["created", "modified", "category_video_count"]

    def category_video_count(self, obj):
        return obj.videos.count()
    category_video_count.short_description = "Number of videos"
