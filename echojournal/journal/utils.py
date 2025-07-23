# journal/utils.py
from .models import JournalMode

def get_current_mode(request):
    mode_id = request.session.get("current_mode_id")
    if not mode_id:
        return None
    try:
        return JournalMode.objects.get(id=mode_id)
    except JournalMode.DoesNotExist:
        return None
