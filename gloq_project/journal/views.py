import json

from django.contrib import messages
from django.core.mail.backends import console
from django.utils.timezone import now
import pytz
from django.shortcuts import render, redirect
from .forms import JournalEntryForm
from .models import JournalEntry, JournalMode
from django.template.loader import render_to_string
from django.http import HttpResponse
# from openai import OpenAI
from groq import Groq
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.template.loader import render_to_string
from django.http import JsonResponse
from userprofile.models import UserProfile
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.timezone import now, localtime
from django.template.loader import render_to_string
from django.utils.dateparse import parse_date
from django.utils import timezone as dj_timezone
from datetime import datetime, time
from pytz import timezone, UTC
from django.shortcuts import get_object_or_404
from .utils import get_current_mode, set_mode_for_user, get_mode_styler_context, get_active_mode, get_synthesis_prompt

from django.views.decorators.http import require_POST



@login_required
def load_insight_panel(request):
    return render(request, 'journal/insights/insight_panel.html')

@login_required
def load_insight_tab(request, tab_name):
    # You can route logic here later, for now just echo the tab
    return render(request, f'journal/insights/_{tab_name}.html')


def generate_summary_by_mode_and_type(entries, mode_slug, synthesis_type):
    client = Groq(api_key=settings.GROQ_API_KEY)

    # Get the right prompt for mode + type combination
    prompt = get_synthesis_prompt(mode_slug, synthesis_type)

    # Add entries to prompt
    for entry in entries:
        prompt += f"\nDate: {entry.created_at.strftime('%Y-%m-%d %H:%M')}\n"
        prompt += f"Entry: {entry.content}\n"

    response = client.chat.completions.create(
        model="compound-beta-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500,
    )

    return response.choices[0].message.content


@require_GET
def synthesize_entries(request):
    # Get parameters
    synthesis_type = request.GET.get('type', 'reflect')  # Default to reflect
    mode_slug = get_active_mode(request)  # Get current mode

    entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')
    if not entries:
        return HttpResponse("No entries yet to summarize.", status=400)

    # Generate based on mode + type combination
    summary = generate_summary_by_mode_and_type(entries, mode_slug, synthesis_type)

    return render(request, 'journal/_synthesis.html', {
        'synthesis': summary,
        'synthesis_type': synthesis_type,
        'mode': mode_slug
    })


def extract_tags(entry):
    client = Groq(api_key=settings.GROQ_API_KEY)

    prompt = (
        "You are a journaling assistant. Based on the following entry, return a concise list of emotional or thematic "
        "tags that reflect the core content. Examples: 'burnout', 'inspiration', 'routine', 'loneliness'. "
        "Only return a JSON list of tags, like: [\"tag1\", \"tag2\", ...]\n\n"
    )

    prompt += f"- {entry.content.strip()}\n"

    response = client.chat.completions.create(
        model="compound-beta-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=150,
    )

    try:
        tag_list = json.loads(response.choices[0].message.content.strip())
        return tag_list[:2] if isinstance(tag_list, list) else []
    except Exception as e:
        print("Tag extraction failed:", e)
        return []


 # Assumes you have a helper to tag entries

def get_session_timezone(request):
    tzname = request.session.get('timezone')
    if tzname in pytz.all_timezones:
        return timezone(tzname)
    return UTC






# 1. MAIN DASHBOARD VIEW
@login_required
def journal_dashboard(request):
    print("===== DASHBOARD DEBUG START =====")

    # Debug session state
    session_selected_mode_slug = request.session.get("selected_mode_slug")
    session_preferred_mode_slug = getattr(request.user.userprofile.preferred_mode, "slug", None)

    print(f"DEBUG: Session 'selected_mode_slug' = {session_selected_mode_slug}")
    print(f"DEBUG: UserProfile 'preferred_mode_slug' = {session_preferred_mode_slug}")

    # Determine active_mode
    active_mode = get_active_mode(request)
    print(f"DEBUG: Resolved active_mode = {active_mode} (id={getattr(active_mode, 'id', None)})")

    # Prepare other data
    form = JournalEntryForm()
    today = now().date()
    entries_today = JournalEntry.objects.filter(user=request.user, created_at__date=today).order_by('-created_at')
    can_add = entries_today.count() < 3
    modes = JournalMode.objects.filter(is_active=True).order_by('name')
    mode_styler = get_mode_styler_context(active_mode)

    print(f"DEBUG: Entries today count = {entries_today.count()}")
    print(f"DEBUG: Can add more entries today? = {can_add}")
    print("===== DASHBOARD DEBUG END =====")

    return render(request, 'dashboard.html', {
        'form': form,
        'entries': entries_today,
        'active_mode': active_mode,
        'modes': modes,
        'can_add': can_add,
        'user_timezone': str(get_session_timezone(request)),
        'mode_styler': mode_styler,
    })



@login_required
def mode_selector(request):
    modes = JournalMode.objects.filter(is_active=True).order_by('name')
    print('Current Mode:' + str(get_current_mode(request)))
    return render(request, "journal/partials/_mode_selector.html", {'modes': modes})


@login_required
def mode_explorer(request):
    modes = JournalMode.objects.all()
    active_mode = get_active_mode(request)
    mode_styler = get_mode_styler_context(active_mode)
    return render(request, "journal/mode_explorer.html", {
        "modes": modes,
        "active_mode": active_mode,
        'mode_styler': mode_styler,
    })


@login_required
@require_POST
def switch_mode_dynamic(request):
    mode_slug = request.POST.get('mode_slug')
    if not mode_slug:
        return HttpResponseBadRequest("No mode selected")

    try:
        mode = JournalMode.objects.get(slug=mode_slug, is_active=True)
        # Update session only
        request.session['selected_mode_slug'] = mode.slug

        # Get updated context
        mode_styler = get_mode_styler_context(mode_slug)

        # Return multiple HTMX updates
        response = HttpResponse()
        response['HX-Trigger-After-Swap'] = json.dumps({
            "updateTheme": {
                "mode_slug": mode_slug,
                "background_class": mode_styler['background_class'],
                "mode_name": mode.name
            }
        })
        return response

    except JournalMode.DoesNotExist:
        return HttpResponseBadRequest("Invalid mode")


@login_required
def set_selected_mode(request, mode_slug):
    mode = get_object_or_404(JournalMode, slug=mode_slug)
    request.session['selected_mode_slug'] = mode.slug
    return redirect("journal:mode_explorer")

@login_required
def set_preferred_mode(request, mode_slug):
    mode = get_object_or_404(JournalMode, slug=mode_slug)
    userprofile = request.user.userprofile
    userprofile.preferred_mode = mode
    userprofile.save()
    return redirect("journal:mode_explorer")

# @login_required
# def mode_explorer(request):
#     modes = JournalMode.objects.all()
#     if request.method == "POST":
#         selected_mode_id = request.POST.get("mode_id")
#         profile = request.user.userprofile
#         profile.selected_mode_id = selected_mode_id
#         profile.save()
#         return redirect('journal_dashboard')
#
#     return render(request, 'journal/mode_explorer.html', {'modes': modes})

@login_required
@require_POST
def _mode_banner(request):
    mode_slug = request.POST.get("slug")  # Get from POST data
    if not mode_slug:
        mode_slug = get_active_mode(request)  # Fallback to session

    print(f"DEBUG: SLUG: = {mode_slug}")
    mode = get_object_or_404(JournalMode, slug=mode_slug)
    # Don't update session here - switch_mode_dynamic already did it

    mode_styler = get_mode_styler_context(mode_slug)
    return render(request, "journal/_mode_banner.html", {
        "mode_styler": mode_styler,
        'selected_mode': mode,
    })


@login_required
@require_POST
def _synth_button(request):
    mode_slug = request.POST.get("slug")
    if not mode_slug:
        mode_slug = get_active_mode(request)

    mode = get_object_or_404(JournalMode, slug=mode_slug)
    mode_styler = get_mode_styler_context(mode_slug)

    return render(request, "journal/_synthesize_buttons.html", {
        "mode_styler": mode_styler,
        'selected_mode': mode,
    })


@login_required
@require_POST
def _entry_filter(request):
    mode_slug = request.POST.get("slug")  # Get from POST data
    if not mode_slug:
        mode_slug = get_active_mode(request)  # Fallback to session

    print(f"DEBUG: SLUG: = {mode_slug}")
    mode = get_object_or_404(JournalMode, slug=mode_slug)
    # Don't update session here - switch_mode_dynamic already did it

    mode_styler = get_mode_styler_context(mode_slug)
    return render(request, "journal/_entry_filter.html", {
        "mode_styler": mode_styler,
        'selected_mode': mode,
    })

@require_POST
@login_required
def set_journal_mode(request):
    mode_slug = request.POST.get('mode')
    try:
        mode = JournalMode.objects.get(slug=mode_slug)
        set_mode_for_user(request, mode)
        return JsonResponse({'status': 'success', 'mode': mode.name})
    except JournalMode.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid mode'})

def journal_entry_by_mode(request, slug):
    mode = get_object_or_404(JournalMode, slug=slug)
    request.session['selected_mode'] = mode.slug  # or mode.id if you prefer
    return redirect('journal:journal_dashboard')  # We'll adapt the entry view soon

# 2. NEW JOURNAL ENTRY VIEW (HTMX endpoint)

@require_POST
@login_required
def submit_journal_entry(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request."}, status=400)

    today = now().date()
    entries_today = JournalEntry.objects.filter(user=request.user, created_at__date=today)

    if entries_today.count() >= 3:
        return JsonResponse({
            "error": "Daily entry limit reached."
        }, status=400)

    form = JournalEntryForm(request.POST)
    if form.is_valid():
        entry = form.save(commit=False)
        entry.user = request.user
        entry.save()

        # Tagging and save again
        entry.tags = extract_tags(entry)
        entry.save()

        return JsonResponse({
            "success": True,
            "message": "Journal entry saved successfully!",
            "entry_id": entry.id
        })
    else:
        return JsonResponse({
            "error": "Please correct the errors in the form.",
            "form_errors": form.errors
        }, status=400)
# def submit_journal_entry(request):
#     if request.method != "POST":
#         return HttpResponseBadRequest("Invalid request.")
#
#     today = now().date()
#     entries_today = JournalEntry.objects.filter(user=request.user, created_at__date=today)
#
#     if entries_today.count() >= 3:
#         html = render_to_string("journal/partials/_alert.html", {
#             "type": "danger",
#             "message": "Daily entry limit reached.",
#         })
#         return HttpResponse(html, status=400)
#
#     form = JournalEntryForm(request.POST)
#     if form.is_valid():
#         entry = form.save(commit=False)
#         entry.user = request.user
#         entry.save()
#
#         # Tagging and save again
#         entry.tags = extract_tags(entry)
#         entry.save()
#
#         entries_today = JournalEntry.objects.filter(user=request.user, created_at__date=today).order_by('-created_at')
#         can_add = entries_today.count() < 3
#
#         entries_html = render_to_string("journal/_entries.html", {
#             'entries': entries_today,
#             'can_add': can_add,
#         }, request=request)
#
#         alert_html = render_to_string("journal/partials/_alert.html", {
#             "type": "success",
#             "message": "Journal entry saved successfully!",
#         })
#
#         return HttpResponse(alert_html + entries_html)
#     else:
#         error_html = render_to_string("journal/partials/_alert.html", {
#             "type": "danger",
#             "message": "Please correct the errors in the form.",
#         })
#         return HttpResponse(error_html, status=400)


@login_required
def same_day_entries(request):
    today = now().date()

    entries = JournalEntry.objects.filter(
        user=request.user,
        created_at__date=today
    ).order_by('-created_at')

    can_add = entries.count() < 3

    html = render_to_string("journal/_entries.html", {
        'entries': entries,
        'can_add': can_add,
    }, request=request)

    return HttpResponse(html)





@login_required
def filter_entries_by_date(request):
    date_str = request.GET.get('entry-date')
    if not date_str:
        return HttpResponseBadRequest("Missing date.")

    entry_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    start = dj_timezone.make_aware(datetime.combine(entry_date, time.min))
    end = dj_timezone.make_aware(datetime.combine(entry_date, time.max))

    entries = JournalEntry.objects.filter(user=request.user, created_at__range=(start, end)).order_by('-created_at')

    return render(request, 'journal/_entries.html', {
        'entries': entries,
        'can_add': entries.count() < 3,
    })


