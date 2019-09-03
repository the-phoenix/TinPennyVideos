from django.contrib import admin
from .models import Snippet


# Register your models here.
class SnippetsAdmin(admin.ModelAdmin):
    readonly_fields = ('highlighted', )


admin.site.register(Snippet, SnippetsAdmin)