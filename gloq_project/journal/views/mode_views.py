from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json

from ..context_processors import active_mode
from ..models import JournalMode
from ..utils import get_active_mode, set_mode_for_user, get_mode_styler_context, get_header_config, get_current_mode
from ..mode_styler import get_feature_styles, get_card_icons
from ..utils import get_daily_content





@require_POST
def mode_banner(request):
    active_mode = get_active_mode(request)

    # Handle POST override - this should OVERRIDE the active mode temporarily
    mode_slug = request.POST.get("slug")
    if mode_slug:
        # User is explicitly switching modes via POST
        mode = get_object_or_404(JournalMode, slug=mode_slug)
        # Optionally update session to remember this choice
        request.session['selected_mode_id'] = mode.id
    else:
        # Use your active mode logic (preferred mode for new sessions, etc.)
        mode = active_mode or get_object_or_404(JournalMode, slug='default')
    mode_header = get_header_config(active_mode)
    return render(request, "journal/modes/_mode_banner.html", {'mode_header': mode_header, 'mode':mode})


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
    return render(request, "journal/modes/mode_explorer.html", {
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
                # "background_class": mode_styler['background_class'],
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
# def mode_selector(request):
#     modes = JournalMode.objects.filter(is_active=True).order_by('name')
#     return render(request, "journal/partials/_mode_selector.html", {'modes': modes})
#
# @login_required
# def mode_explorer(request):
#     modes = JournalMode.objects.all()
#     active_mode = get_active_mode(request)
#     mode_styler = get_mode_styler_context(active_mode)
#     return render(request, "journal/modes/mode_explorer.html", {"modes": modes, "active_mode": active_mode, 'mode_styler': mode_styler})
#
# @login_required
# @require_POST
# def switch_mode_dynamic(request):
#     mode_slug = request.POST.get('mode_slug')
#     if not mode_slug:
#         return HttpResponseBadRequest("No mode selected")
#     try:
#         mode = JournalMode.objects.get(slug=mode_slug, is_active=True)
#         request.session['selected_mode_slug'] = mode.slug
#         response = HttpResponse()
#         response['HX-Trigger-After-Swap'] = json.dumps({"updateTheme": {"mode_slug": mode_slug, "mode_name": mode.name}})
#         return response
#     except JournalMode.DoesNotExist:
#         return HttpResponseBadRequest("Invalid mode")
#
#
# @login_required
# def set_selected_mode(request, mode_slug):
#     mode = get_object_or_404(JournalMode, slug=mode_slug)
#     request.session['selected_mode_slug'] = mode.slug
#     return redirect("journal:mode_explorer")
#
# @login_required
# def set_preferred_mode(request, mode_slug):
#     mode = get_object_or_404(JournalMode, slug=mode_slug)
#     userprofile = request.user.userprofile
#     userprofile.preferred_mode = mode
#     userprofile.save()
#     return redirect("journal:mode_explorer")


@login_required
@require_POST
def _mode_features(request):
    # Get the active mode from context processor (your logic for new sessions, etc.)
    active_mode = get_active_mode(request)

    # Handle POST override - this should OVERRIDE the active mode temporarily
    mode_slug = request.POST.get("slug")
    if mode_slug:
        # User is explicitly switching modes via POST
        mode = get_object_or_404(JournalMode, slug=mode_slug)
        # Optionally update session to remember this choice
        request.session['selected_mode_id'] = mode.id
    else:
        # Use your active mode logic (preferred mode for new sessions, etc.)
        mode = active_mode or get_object_or_404(JournalMode, slug='default')

    # Use the mode's slug for styling functions
    mode_styler = get_mode_styler_context(active_mode)
    mode_header = get_header_config(active_mode)
    feature_styles = get_feature_styles(active_mode)
    feature_content = get_daily_content(request, mode_slug)
    card_icons = get_card_icons()
    print(f"DEBUG: Resolved active_mode features = {active_mode}")
    return render(request, "journal/modes/_mode_features.html", {
        "mode_styler": mode_styler,
        'mode_header': mode_header,
        'selected_mode': mode,
        'feature_styles': feature_styles,
        'feature_content': feature_content,
        'card_icons': card_icons,
    })