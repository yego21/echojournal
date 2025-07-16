from django.contrib import admin
from .models import JournalEntry

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'start_entry', 'midday_entry', 'end_entry')
    list_filter = ('user', 'date')
    search_fields = ('start_entry', 'midday_entry', 'end_entry')
