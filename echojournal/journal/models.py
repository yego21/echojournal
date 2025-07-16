from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField  # if using Postgres

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    start_entry = models.TextField()
    midday_entry = models.TextField(blank=True)
    end_entry = models.TextField(blank=True)
    tags = ArrayField(models.CharField(max_length=50), blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
