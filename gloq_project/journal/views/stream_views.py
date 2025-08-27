from django.shortcuts import render


def stream_content(request):
    return render(request, "journal/stream/note_stream.html")