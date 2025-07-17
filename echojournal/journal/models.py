from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField  # if using Postgres

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=20, null=True, blank=True)  # 'entry1', 'entry2', 'entry3'
    content = models.TextField()
    tags = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

    class Meta:
        ordering = ['-created_at']
