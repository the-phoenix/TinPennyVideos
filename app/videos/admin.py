from django.contrib import admin
from .models import Video


# Register your models here.
class VideosAdmin(admin.ModelAdmin):
    readonly_fields = ('stream_url', 'source_size_in_kb', 'duration_in_seconds')


admin.site.register(Video, VideosAdmin)