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


def generate_summary(entries):
    # client = OpenAI(api_key=settings.OPENAI_API_KEY)
    client = Groq(api_key=settings.GROQ_API_KEY)
    # print("Loaded API key:", settings.OPENAI_API_KEY)

    prompt = "You are a genius that notices patterns that people may not see, you always get the gist based on user entries and hints them as to what they might need and want. You also cheer them up on your own way, often backhanded.\n\n"
    for entry in entries:
        prompt += f"\nDate: {entry.date}\n"
        prompt += f"Start: {entry.start_entry}\n"
        prompt += f"Midday: {entry.midday_entry}\n"
        prompt += f"End: {entry.end_entry}\n"
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

    prompt = "You are a journaling assistant. Based on the following entries, return a concise list of emotional or thematic tags that reflect the core content. Examples: 'burnout', 'inspiration', 'routine', 'loneliness'. Only return a JSON list of tags, like: [\"tag1\", \"tag2\", ...]\n\n"

    for entry in entries:
        prompt += f"\nDate: {entry.date}\nStart: {entry.start_entry}\nMid: {entry.midday_entry}\nEnd: {entry.end_entry}\n"

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

@login_required
def journal_entry(request):
    form = JournalEntryForm(request.POST or None)
    entries = JournalEntry.objects.filter(user=request.user).order_by('-date')[:5]

    if request.method == "POST" and 'submit_entry' in request.POST:
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user  # make sure user is set
            entry.save()

            # Tag it after saving
            tags = extract_tags([entry])
            entry.tags = tags
            entry.save()


            entries = JournalEntry.objects.filter(user=request.user).order_by('-date')[:5]

            if request.headers.get('Hx-Request'):
                html = render_to_string('journal/_entries.html', {'entries': entries})
                return HttpResponse(html)
            return redirect('journal_entry')

    return render(request, 'dashboard.html', {
        'form': form,
        'entries': entries,
    })


@require_GET
def synthesize_entries(request):
    entries = JournalEntry.objects.order_by('-date')
    if not entries:
        return HttpResponse("No entries yet to summarize.", status=400)

    summary = generate_summary(entries)

    return render(request, 'journal/_synthesis.html', {
        'synthesis': summary
    })
