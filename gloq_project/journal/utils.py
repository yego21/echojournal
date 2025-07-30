# journal/utils.py
from .models import JournalMode
from .mode_styler import MODE_STYLER_CONFIG


def get_synthesis_prompt(mode_slug, synthesis_type):
    SYNTHESIS_PROMPTS = {
        'mystical': {
            'reflect': "You are a wise mystic who sees deeper spiritual patterns...",
            'digest': "As an intuitive guide, summarize the cosmic patterns...",
            'roast': "Channel your inner cosmic trickster and playfully call out...",
            'suggest': "As a spiritual advisor, suggest mystical practices..."
        },
        'philosophical': {
            'reflect': "You are a thoughtful philosopher who examines life's deeper meanings...",
            'digest': "Analyze these thoughts with philosophical rigor...",
            'roast': "Be a brutally honest Socratic questioner...",
            'suggest': "Suggest philosophical exercises and deeper questions..."
        }
        # Add more modes as needed
    }
    return SYNTHESIS_PROMPTS.get(mode_slug, {}).get(synthesis_type, "Default prompt...")

def get_preferred_mode(user):
    preferred_mode = getattr(user.profile, 'preferred_mode', None)
    return preferred_mode.slug if preferred_mode else None

def get_selected_mode(request):
    mode_slug = request.session.get('selected_mode_slug')
    if mode_slug:
        try:
            return JournalMode.objects.get(slug=mode_slug)
        except JournalMode.DoesNotExist:
            pass
    return None

def get_active_mode(request):
    # Try session-selected mode
    selected_mode_slug = request.session.get("selected_mode_slug")
    if selected_mode_slug:
        mode = JournalMode.objects.filter(slug=selected_mode_slug, is_active=True).first()
        if mode:
            return mode.slug

    # Fallback to preferred mode
    if request.user.is_authenticated:
        userprofile = getattr(request.user, 'userprofile', None)
        if userprofile and userprofile.preferred_mode and userprofile.preferred_mode.is_active:
            return userprofile.preferred_mode.slug

    return None

def get_current_mode(request):
    # FUTURE: Allow session-based preview override
    if 'selected_mode' in request.session:
        return request.session['selected_mode']

    # Default: fallback to user preference
    if request.user.is_authenticated:
        return getattr(request.user.profile, 'preferred_mode', 'default_mode')


    # Guest fallback
    return 'default_mode'
    # mode_id = request.session.get("current_mode_id")
    # if not mode_id:
    #     print("DEBUG: No current_mode_id found in session.")
    #     return None
    # try:
    #     print(f"DEBUG: Retrieved Mode from session → ID: {mode.id}, Slug: '{mode.slug}'")
    #     return JournalMode.objects.get(id=mode_id)
    # except JournalMode.DoesNotExist:
    #     print(f"DEBUG: Mode with ID {mode_id} not found in DB.")
    #     return None

def set_mode_for_user(request, mode):
    request.session['selected_mode'] = mode.slug
    request.session['current_mode_id'] = mode.id  # ← Make sure you're setting this
    print(f"DEBUG: Mode set → ID: {mode.id}, Slug: '{mode.slug}'")

    if request.user.is_authenticated:
        profile = request.user.profile
        profile.preferred_mode = mode
        profile.save()
        print(f"DEBUG: User profile updated with preferred mode → ID: {mode.id}, Slug: '{mode.slug}'")

def get_mode_styler_context(current_mode):
    """Return CSS class mappings based on the current mode."""
    if current_mode in MODE_STYLER_CONFIG:
        return MODE_STYLER_CONFIG[current_mode]
    return MODE_STYLER_CONFIG['default']