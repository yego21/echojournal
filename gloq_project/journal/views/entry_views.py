from groq import Groq
from django.conf import settings
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

from ..models import JournalEntry, Tag
from ..forms import JournalEntryForm


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

        # Extract tags
        extracted_tags = extract_tags(entry)

        for tag_name in extracted_tags:
            tag_obj, created = Tag.objects.get_or_create(name=tag_name)
            entry.tags.add(tag_obj)

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