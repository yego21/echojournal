from django.contrib import admin
from .models import JournalEntry


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'label', 'short_content', 'created_at')
    list_filter = ('user', 'label', 'created_at')
    search_fields = ('content', 'tags')

    def short_content(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    short_content.short_description = 'Content Preview'
