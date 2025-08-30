from django.urls import path
from . import views
from .views.dashboard_views import journal_dashboard
from .views.mode_views import mode_explorer, _mode_features, mode_selector, set_selected_mode, set_preferred_mode, switch_mode_dynamic, mode_banner
from .views.search_views import search_modal, search_results, filter_results_by_tag, entry_detail
from .views.stream_views import stream_content
from .views.refraction_views import synthesize_entries, load_insight_panel, load_insight_tab
from .views.entry_views import submit_journal_entry

app_name = "journal"

urlpatterns = [
    # --- Dashboard & Entries ---
    path("", journal_dashboard, name="journal_dashboard"),
    path("entries/new/", submit_journal_entry, name="new_journal_entry"),
    path("entry/<int:pk>/", entry_detail, name="entry_detail"),
    path("synthesize/", synthesize_entries, name="synthesize_entries"),

    # --- Modes & Preferences ---
    path("mode_banner/", mode_banner, name="mode_banner"),
    path("modes/", mode_explorer, name="mode_explorer"),
    path("_mode_features/", _mode_features, name="_mode_features"),
    path("set-selected-mode/<mode_slug>/", set_selected_mode, name="set_selected_mode"),
    path("set-preferred-mode/<mode_slug>/", set_preferred_mode, name="set_preferred_mode"),
    path("switch-mode-dynamic/", switch_mode_dynamic, name="switch_mode_dynamic"),

    # --- Insights ---
    path("insight-panel/", load_insight_panel, name="load_insight_panel"),
    path("insight-tab/<str:tab_name>/", load_insight_tab, name="load_insight_tab"),

    # --- Search ---
    path("search/modal/", search_modal, name="search_modal"),
    path("search/results/", search_results, name="search_results"),
    path("search/results_by_tag/", filter_results_by_tag, name="filter_results_by_tag"),

    # --- Streaming ---
    path("stream/", stream_content, name="stream_content"),
]