import logging
from functools import wraps

from django.utils import translation
from django.utils.translation import gettext as _
from django.views.generic.base import View
from rest_framework import status

from apps.core.constants import AUTH_TOKEN_HEADER_NAME
from apps.core.utils.keycloak_client import KeyCloakClient
from apps.core.utils.web_utils import WebUtils

logger = logging.getLogger("apps")


class HasRole(object):
    """
    decorator. log exception if task_definition has
    """

    def __init__(self, roles=None):
        if roles is None:
            roles = ["admin"]
        self.roles = roles

    def __call__(self, task_definition):
        @wraps(task_definition)
        def wrapper(*args, **kwargs):
            request = args[0]
            if isinstance(request, View):
                request = args[1]
            token = request.META.get(AUTH_TOKEN_HEADER_NAME)
            translation.activate(request.COOKIES.get("lang", "zh-hans"))
            if token is None:
                return WebUtils.response_error(
                    error_message=_("please provide Token"),
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )
            client = KeyCloakClient()
            is_active, user_info = client.token_is_valid(token)
            if not is_active:
                return WebUtils.response_error(
                    error_message=_("token validation failed"),
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )
            roles = user_info["realm_access"]["roles"]
            for i in roles:
                if i in self.roles:
                    return task_definition(*args, **kwargs)
            return WebUtils.response_error(
                error_message=_("insufficient permissions"),
                status_code=status.HTTP_403_FORBIDDEN,
            )

        return wrapper
