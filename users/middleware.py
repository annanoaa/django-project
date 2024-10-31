from django.utils import timezone
from django.contrib.auth.decorators import login_required

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user.last_active_datetime = timezone.now()
            request.user.save()
        return self.get_response(request)