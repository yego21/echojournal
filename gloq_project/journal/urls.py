from django.urls import path
from . import views


app_name = "journal"

urlpatterns = [
    path('', views.journal_dashboard, name='journal_dashboard'),
    path('entries/', views.same_day_entries, name='same_day_entries'),
    path('entries/new/', views.submit_journal_entry, name='new_journal_entry'),
    path('synthesize/', views.synthesize_entries, name='synthesize_entries'),
    # path('fetch-entries/', views.fetch_entries_by_range, name='fetch_entries_by_range'),



    path('modes/', views.mode_explorer, name='mode_explorer'),
    path('_mode_banner/', views._mode_banner, name='_mode_banner'),
    path("_synth_button/", views._synth_button, name="_synth_button"),
    path("_entry_filter/", views._entry_filter, name="_entry_filter"),
    path("_mode_features/", views._mode_features, name="_mode_features"),
    path('mode/<slug:slug>/', views.journal_entry_by_mode, name='journal_entry_by_mode'),
    path('mode-selector/', views.mode_selector, name='mode_selector'),
    path("set-selected-mode/<mode_slug>/", views.set_selected_mode, name="set_selected_mode"),
    path("set-preferred-mode/<mode_slug>/", views.set_preferred_mode, name="set_preferred_mode"),
    path('switch-mode-dynamic/', views.switch_mode_dynamic, name='switch_mode_dynamic'),
    path('insight-panel/', views.load_insight_panel, name='load_insight_panel'),
    path('insight-tab/<str:tab_name>/', views.load_insight_tab, name='load_insight_tab'),


    path("search/modal/", views.search_modal, name="search_modal"),
    path("search/results/", views.search_results, name="search_results"),
    path("search/results_by_tag/", views.filter_results_by_tag, name="filter_results_by_tag"),

    path("entry/<int:pk>/", views.entry_detail, name="entry_detail"),

]
