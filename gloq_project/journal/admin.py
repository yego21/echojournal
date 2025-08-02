from django.contrib import admin
from .models import JournalEntry, JournalMode, DailyContent


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'label', 'short_content', 'created_at')
    list_filter = ('user', 'label', 'created_at')
    search_fields = ('content', 'tags')

    def short_content(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    short_content.short_description = 'Content Preview'

@admin.register(JournalMode)
class JournalModeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_premium', 'is_active', 'created_at')
    list_filter = ('is_premium', 'is_active')


@admin.register(DailyContent)
class DailyContentAdmin(admin.ModelAdmin):
    list_display = ('mode', 'date', 'content_type', 'personalization_key', 'content_data', 'created_at' )

