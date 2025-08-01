# journal/utils.py
import json

import pytz

from .models import JournalMode
from .mode_styler import MODE_STYLER_CONFIG
from groq import Groq
import random
from datetime import datetime
import os
from django.core.cache import cache

def get_synthesis_prompt(mode_slug, synthesis_type):
    SYNTHESIS_PROMPTS = {
        "mystical": {
            "reflect": "Interpret the journal entry through symbols, dreams, and archetypal meaning. Weave in gentle spiritual insights.",
            "digest": "Integrate today’s events into a spiritual lesson. Focus on personal growth and meaning.",
            "roast": "Playfully call out whimsical over-interpretations or magical thinking. Keep it lighthearted.",
            "suggest": "Recommend grounded, soulful next steps for clarity or alignment."
        },
        "philosophical": {
            "reflect": "Contemplate your experiences in light of life's bigger questions and timeless ideas.",
            "digest": "Extract deep lessons or moral insights from today’s events in a thoughtful, reasoned tone.",
            "roast": "Wittily point out contradictions, flawed reasoning, or philosophical overcomplication.",
            "suggest": "Offer a thought-provoking question or perspective for tomorrow’s reflection."
        },
        "medical": {
            "reflect": "Consider how today’s choices have influenced your physical, mental, and emotional health.",
            "digest": "Summarize health-related patterns you’ve noticed and what they reveal.",
            "roast": "Gently poke fun at health slips or over‑the‑top wellness attempts.",
            "suggest": "Give a simple, actionable health tip or self-care adjustment for tomorrow."
        },
        "creative": {
            "reflect": "Explore today’s events as if they were part of a story, poem, or artistic expression.",
            "digest": "Identify creative sparks or themes emerging from your day.",
            "roast": "Humorously exaggerate or remix moments into over‑the‑top creative takes.",
            "suggest": "Offer a playful creative challenge or artistic prompt for tomorrow."
        },
        "productive": {
            "reflect": "Assess how your time and energy were spent toward meaningful progress today.",
            "digest": "Summarize what worked and what slowed you down in achieving your goals.",
            "roast": "Point out amusing inefficiencies, procrastination traps, or over‑optimization.",
            "suggest": "Recommend one small, high‑impact improvement for tomorrow’s productivity."
        },
        "exploratory": {
            "reflect": "Look at today’s events as part of a journey of discovery and learning.",
            "digest": "Highlight new experiences, ideas, or perspectives you gained today.",
            "roast": "Poke fun at curious detours, surprising finds, or ‘how did I end up here?’ moments.",
            "suggest": "Propose a small experiment or new path to explore tomorrow."
        },
        "visionary": {
            "reflect": "Frame today’s experiences in the context of your long‑term dreams and aspirations.",
            "digest": "Pull out the themes and steps that connect your present actions to your future vision.",
            "roast": "Wittily point out grand plans that clash with today’s reality.",
            "suggest": "Offer a motivating, future‑focused step for tomorrow that keeps your vision alive."
        }
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



from datetime import datetime
from django.core.cache import cache
import random
import os
from groq import Groq
import pytz

def get_daily_philosophy_content(request):
    """Get a daily philosophical question + fact, cached for 24h per user timezone."""

    # Get user's local timezone
    user_tz = getattr(request.user.profile, 'timezone', 'UTC') or 'UTC'
    tz = pytz.timezone(user_tz)
    today_str = datetime.now(tz).strftime('%Y-%m-%d')

    # Cache key is unique to date + user timezone
    cache_key = f"daily_philosophy_content:{today_str}"

    # Check cache first
    cached = cache.get(cache_key)
    if cached:
        print(f"[DEBUG] Using cached daily content: {cached}")
        return cached

    try:
        # Create Groq client
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        # Make **one call** that asks for both
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{
                "role": "user",
                "content": (
                    f"Generate two items for a daily philosophical highlight. "
                    f"1) A concise, thought-provoking philosophical question for self-reflection. "
                    f"2) A short but insightful philosophical fact or idea from history. "
                    f"Make both no more than 1–2 sentences. "
                    f"Return them as JSON with keys 'question' and 'fact'. Today's date is {today_str}."
                )
            }],
            max_tokens=200,
            temperature=0.7
        )

        import json
        content_str = response.choices[0].message.content.strip()
        try:
            data = json.loads(content_str)  # If Groq really returns JSON
        except json.JSONDecodeError:
            # If not perfect JSON, fallback to parsing manually
            data = {
                "question": "What is the true nature of freedom?",
                "fact": "Socrates believed wisdom begins with recognizing one's own ignorance."
            }

        print(f"[DEBUG] Groq returned: {data}")

    except Exception as e:
        print(f"[ERROR] Failed to get Groq content: {e}")

        # Fallback content, seeded for daily consistency
        fallback_questions = [
            "What does it mean to live authentically?",
            "How do we balance personal freedom with social duty?",
            "What role does suffering play in growth?"
        ]
        fallback_facts = [
            "Plato believed reality consists of eternal forms beyond physical perception.",
            "Aristotle argued that virtue is developed through habit and practice.",
            "Nietzsche suggested that meaning must be created, not discovered."
        ]
        random.seed(today_str)  # Keeps same fallback all day
        data = {
            "question": random.choice(fallback_questions),
            "fact": random.choice(fallback_facts)
        }

    # Save to cache for 24 hours
    cache.set(cache_key, data, timeout=60 * 60 * 24)
    return data

def get_daily_mystical_content(request):
    user_tz = getattr(request.user.profile, 'timezone', 'UTC') or 'UTC'
    tz = pytz.timezone(user_tz)
    today_str = datetime.now(tz).strftime('%Y-%m-%d')
    cache_key = f"daily_mystical:{today_str}"
    cached = cache.get(cache_key)
    if cached:
        print(f"[DEBUG] Using cached mystical content: {cached}")
        return cached

    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        prompt = (
            "Return JSON with exactly these keys: "
            "`astronomical` Astronomical notable (if no event, give timeless sky reflection), "
            "`action` Suggested mystical action (personalize if zodiac sign given), "
            "`fact` Mystical fact of the day about magick, alchemy, or esoteric traditions."
                    "Keep each concise and inspiring.. "

        )

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )

        # Debug raw Groq output
        print("[DEBUG] Raw Groq mystical response:", response)

        content = response.choices[0].message.content.strip()
        print("[DEBUG] Extracted content string:", content)

        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            print("[ERROR] Groq did not return valid JSON, falling back.")
            data = {
                "astronomical": "The Moon is waxing, symbolizing growth and intention setting.",
                "action": "Light a candle and meditate for 5 minutes to align with today's lunar energy.",
                "fact": "Alchemy once aimed to transform lead into gold, both literally and spiritually."
            }

    except Exception as e:
        print(f"[ERROR] Failed to get Groq mystical content: {e}")
        data = {
            "astronomical": "The Moon is waxing, symbolizing growth and intention setting.",
            "action": "Light a candle and meditate for 5 minutes to align with today's lunar energy.",
            "fact": "Alchemy once aimed to transform lead into gold, both literally and spiritually."
        }

    cache.set(cache_key, data, timeout=60*60*24)
    return data






def get_daily_content(request, mode):
    if mode == 'philosophical':
        daily = get_daily_philosophy_content(request)
        return {
            'title': '🤔 Philosophical Focus',
            'question_content': daily['question'],
            'fact_content': daily['fact'],
            'subtitle': 'Daily contemplation'
        }
    elif mode == 'mystical':
        daily = get_daily_mystical_content(request)
        print("[DEBUG] Mystical daily data:", daily)  #
        return {
            'title': '🌙 Mystical Focus',
            'astronomical': daily['astronomical'],
            'action': daily['action'],
            'fact': daily['fact']
        }