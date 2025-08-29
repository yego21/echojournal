from django.shortcuts import render

from ..models import JournalEntry

def stream_content(request):
    """Return the stream template with real entries"""
    entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')[:2]
    return render(request, 'journal/stream/note_stream.html', {
        'entries': entries,
        'entries_count': entries.count(),
        # 'ambient_quotes': get_random_older_entries(request.user, 1),
    })



