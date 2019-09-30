import datetime

from django.contrib import admin
from .models import Video, Category, Stream
from .utils import td_format


class StreamAdminInline(admin.TabularInline):
    model = Stream

# Register your models here.
@admin.register(Video)
class VideosAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'origin', 'mc_status', 'duration', 'is_private', 'modified')
    # fields=("origin", "origin_size_in_kb")
    inlines = (StreamAdminInline,)

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
