import datetime

from django.contrib import admin

from .models import Video, Category, Stream, S3PathField
from .utils import td_format
from .widgets import AdminS3PathFieldWidget


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
