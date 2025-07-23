from journal.models import JournalMode

def current_mode(request):
    if request.user.is_authenticated:
        mode = request.session.get('selected_mode')

        if mode:
            try:
                selected_mode = JournalMode.objects.get(slug=mode)
                return {'current_mode': selected_mode}
            except JournalMode.DoesNotExist:
                pass  # falls through to return an empty dict

    return {'current_mode': None}
