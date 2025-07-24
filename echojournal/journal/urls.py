from django.urls import path
from . import views


app_name = "journal"

urlpatterns = [
    path('', views.journal_dashboard, name='journal_dashboard'),
    path('entries/', views.same_day_entries, name='same_day_entries'),
    path('entries/new/', views.submit_journal_entry, name='new_journal_entry'),
    path('synthesize/', views.synthesize_entries, name='synthesize_entries'),
    path('fetch-entries/', views.filter_entries_by_date, name='filter_entries_by_date'),
    path('modes/', views.mode_explorer, name='mode_explorer'),
    path("switch-mode/", views.switch_mode, name="switch_mode"),
    path('mode/<slug:slug>/', views.journal_entry_by_mode, name='journal_entry_by_mode'),
    path('mode-selector/', views.mode_selector, name='mode_selector'),
]
