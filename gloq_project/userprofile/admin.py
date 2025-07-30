from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_mode', 'created_at')
    list_filter = ('preferred_mode', 'created_at')
    search_fields = ('user__username',)
