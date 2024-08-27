from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext as _
from rest_framework import status

from apps.base.models import UserAPISecret
from apps.core.utils.web_utils import WebUtils


class APISecretFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.META.get(settings.API_TOKEN_HEADER_NAME)
        if token is None:
            setattr(request, "api_pass", False)
            return None

        is_exist = UserAPISecret.objects.filter(api_secret=token).exists()
        if is_exist:
            setattr(request, "api_pass", True)
            return None
        return WebUtils.response_error(
            error_message=_("token validation failed"), status_code=status.HTTP_403_FORBIDDEN
        )
