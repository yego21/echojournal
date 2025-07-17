import json

from django.shortcuts import render, redirect
from .forms import JournalEntryForm
from .models import JournalEntry
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
from django.utils.timezone import now
from django.template.loader import render_to_string


def generate_summary(entries):
    client = Groq(api_key=settings.GROQ_API_KEY)

    prompt = (
        "You are a genius that notices patterns that people may not see. "
        "You always get the gist based on user entries and hint them as to what they might need and want. "
        "You also cheer them up in your own way, often backhanded.\n\n"
    )

    for entry in entries:
        prompt += f"\nDate: {entry.created_at.strftime('%Y-%m-%d %H:%M')}\n"
        prompt += f"Entry 1: {entry.content}\n"
        prompt += f"Entry 2: {entry.content}\n"
        prompt += f"Entry 3: {entry.content}\n"

    prompt += "\nSummary:"

    response = client.chat.completions.create(
        model="compound-beta-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500,
    )

    return response.choices[0].message.content


def extract_tags(entries):
    client = Groq(api_key=settings.GROQ_API_KEY)

    prompt = (
        "You are a journaling assistant. Based on the following entries, return a concise list of emotional or thematic "
        "tags that reflect the core content. Examples: 'burnout', 'inspiration', 'routine', 'loneliness'. "
        "Only return a JSON list of tags, like: [\"tag1\", \"tag2\", ...]\n\n"
    )

    for entry in entries:
        prompt += f"\nDate: {entry.created_at.strftime('%Y-%m-%d %H:%M')}\n"
        prompt += f"Entry 1: {entry.content}\n"
        prompt += f"Entry 2: {entry.content}\n"
        prompt += f"Entry 3: {entry.content}\n"

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


# 1. MAIN DASHBOARD VIEW
@login_required
def journal_entry(request):
    form = JournalEntryForm()
    entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')[:5]

    return render(request, 'dashboard.html', {
        'form': form,
        'entries': entries,
    })


# 2. NEW JOURNAL ENTRY VIEW (HTMX endpoint)
@login_required
def new_journal_entry(request):
    today = now().date()
    entries_today = JournalEntry.objects.filter(user=request.user, created_at__date=today)

    if entries_today.count() >= 3:
        html = render_to_string("journal/_alert.html", {
            "type": "danger",
            "message": "Daily entry limit reached.",
        })
        return HttpResponse(html, status=400)

    if request.method == "POST":
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            try:
                entry = form.save(commit=False)
                entry.user = request.user
                entry.save()

                # Tag extraction logic
                tags = extract_tags([entry])
                entry.tags = tags
                entry.save()

                entries_today = JournalEntry.objects.filter(
                    user=request.user, created_at__date=today
                ).order_by('-created_at')

                can_add = entries_today.count() < 3

                entries_html = render_to_string("journal/_entries.html", {
                    'entries': entries_today,
                    'can_add': can_add,
                }, request=request)

                alert_html = render_to_string("journal/_alert.html", {
                    "type": "success",
                    "message": "Journal entry saved successfully!",
                }, request=request)

                full_response = alert_html + entries_html
                return HttpResponse(full_response)

            except Exception as e:
                error_html = render_to_string("journal/_alert.html", {
                    "type": "danger",
                    "message": f"Something went wrong: {str(e)}",
                })
                return HttpResponse(error_html, status=500)

        else:
            error_html = render_to_string("journal/_alert.html", {
                "type": "danger",
                "message": "Please correct the errors in the form.",
            })
            return HttpResponse(error_html, status=400)

    return HttpResponseBadRequest("Invalid request.")


# 3. OPTIONAL: REFRESH ENTRIES LIST (can be used with hx-get)
@login_required
def journal_entries(request):
    entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')[:5]
    can_add = JournalEntry.objects.filter(user=request.user, created_at__date=now().date()).count() < 3

    html = render_to_string("journal/_entries.html", {
        'entries': entries,
        'can_add': can_add,
    }, request=request)

    return HttpResponse(html)


@require_GET
def synthesize_entries(request):
    entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')
    if not entries:
        return HttpResponse("No entries yet to summarize.", status=400)

    summary = generate_summary(entries)

    return render(request, 'journal/_synthesis.html', {
        'synthesis': summary
    })
