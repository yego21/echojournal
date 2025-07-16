from django.urls import path
from . import views

urlpatterns = [
    path('', views.journal_entry, name='journal_entry'),
    path('synthesize/', views.synthesize_entries, name='synthesize_entries'),
]
