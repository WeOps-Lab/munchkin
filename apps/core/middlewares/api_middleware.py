from django.conf import settings
from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext as _
from rest_framework import status

from apps.base.models import User, UserAPISecret
from apps.core.utils.web_utils import WebUtils


class APISecretFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.META.get(settings.API_TOKEN_HEADER_NAME)
        if token is None:
            setattr(request, "api_pass", False)
            return None

        user_secret = UserAPISecret.objects.filter(api_secret=token).first()
        if user_secret:
            setattr(request, "api_pass", True)
            user = User.objects.get(username=user_secret.username)
            auth.login(request, user)
            return None
        return WebUtils.response_error(
            error_message=_("token validation failed"), status_code=status.HTTP_403_FORBIDDEN
        )
