from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField  # if using Postgres

class JournalMode(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    is_premium = models.BooleanField(default=False)  # For future paywalling
    is_active = models.BooleanField(default=True)    # In case some modes are disabled
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mode = models.ForeignKey(JournalMode, on_delete=models.SET_NULL, null=True)
    label = models.CharField(max_length=20, null=True, blank=True)  # 'entry1', 'entry2', 'entry3'
    content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True, related_name="entries")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

    class Meta:
        ordering = ['-created_at']



class DailyContent(models.Model):
    CONTENT_TYPES = [
        ('global', 'Global'),
        ('zodiac', 'Zodiac-specific'),
        ('personalized', 'User-personalized'),
    ]

    mode = models.ForeignKey(JournalMode, on_delete=models.CASCADE)
    date = models.DateField()
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES, default='global')
    personalization_key = models.CharField(max_length=100, blank=True, null=True)
    content_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['mode', 'date', 'content_type', 'personalization_key']
        indexes = [
            models.Index(fields=['mode', 'date', 'content_type']),
        ]

    def __str__(self):
        return f"{self.mode.name} - {self.date} ({self.content_type})"

















