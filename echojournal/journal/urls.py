from django.urls import path
from . import views

urlpatterns = [
    path('', views.journal_entry, name='journal_entry'),
    path('entries/', views.journal_entries, name='journal_entries'),
    path('entries/new/', views.new_journal_entry, name='new_journal_entry'),
    path('synthesize/', views.synthesize_entries, name='synthesize_entries'),
]
