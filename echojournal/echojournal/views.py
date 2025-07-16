from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def landing_or_dashboard(request):
    if request.user.is_authenticated:
        return redirect('journal_entry')  # Or 'dashboard'
    return render(request, 'landing.html')

def logout_view(request):
    logout(request)

    if request.headers.get('HX-Request'):
        return JsonResponse({"redirect": True, "redirect_url": ""})  # or 'login' or any landing page
    else:
        # For non-HTMX requests, do a standard redirect.

        return redirect('landing_or_dashboard')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('journal_entry')
    else:
        form = UserCreationForm()
    return render(request, 'user_management/signup.html', {'form': form})