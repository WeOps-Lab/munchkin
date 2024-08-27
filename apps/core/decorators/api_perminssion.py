import logging
from functools import wraps

from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext as _
from django.views.generic.base import View

from apps.core.utils.keycloak_client import KeyCloakClient
from apps.core.utils.web_utils import WebUtils

logger = logging.getLogger("app")


class HasRole(object):
    """
    decorator. log exception if task_definition has
    """

    def __init__(self, roles=None):
        if roles is None:
            roles = []
        self.roles = roles

    def __call__(self, task_definition):
        @wraps(task_definition)
        def wrapper(*args, **kwargs):
            request = args[0]
            if isinstance(request, View):
                request = args[1]
            token = request.META.get(settings.AUTH_TOKEN_HEADER_NAME).split("Bearer ")[-1]

            if token is None:
                return WebUtils.response_401(_("please provide Token"))
            client = KeyCloakClient()
            is_active, user_info = client.token_is_valid(token)
            if not is_active:
                return WebUtils.response_401(_("token validation failed"))
            if not self.roles:
                return wrapper
            roles = user_info["realm_access"]["roles"]
            if user_info.get("locale"):
                translation.activate(user_info["locale"])
            for i in roles:
                if i in self.roles:
                    return task_definition(*args, **kwargs)
            return WebUtils.response_403(_("insufficient permissions"))

        return wrapper
