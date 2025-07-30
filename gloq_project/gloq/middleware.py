from django.utils import timezone

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tz = request.session.get('timezone')
        if tz:
            timezone.activate(tz)
        else:
            timezone.deactivate()
        return self.get_response(request)