import datetime

from django.contrib import admin
from .models import Video
from .utils import td_format


# Register your models here.
class VideosAdmin(admin.ModelAdmin):
    readonly_fields = ('stream_path', 'source_size_in_kb', 'duration_in_ms')
    list_display = ('id', 'title', 'source_path', 'stream_path', 'duration', 'is_private', 'modified')

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(VideosAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'source_path':
            field.widget.attrs['class'] = 'vURLField'
        return field

    def duration(self, obj):
        if obj.duration_in_ms is None:
            return None

        return td_format(datetime.timedelta(milliseconds=obj.duration_in_ms))

    duration.admin_order_field = 'duration_in_ms'


admin.site.register(Video, VideosAdmin)
