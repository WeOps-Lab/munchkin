import logging

from django.conf import settings
from django.contrib import auth
from django.core.cache import caches
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext as _

from apps.core.utils.web_utils import WebUtils

cache = caches["db"]


class KeyCloakAuthMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def set_userinfo(request, user):
        """设置用户信息"""
        request.userinfo = {
            "username": user.username,
            "email": user.email,
            "roles": user.roles,
            "group_list": user.group_list,
            "is_superuser": user.is_superuser,
        }

    def process_view(self, request, view, args, kwargs):
        token = request.META.get(settings.AUTH_TOKEN_HEADER_NAME)
        if token is None:
            return WebUtils.response_401(_("please provide Token"))
        token = token.split("Bearer ")[-1]
        session_key = request.session.session_key
        if session_key:
            cache_token = cache.get(session_key)
            if cache_token == token:
                return None
        user = auth.authenticate(request=request, token=token)
        if user is not None:
            auth.login(request, user)
            session_key = request.session.session_key
            if not session_key:
                request.session.cycle_key()
            session_key = request.session.session_key
            cache.set(session_key, token, settings.LOGIN_CACHE_EXPIRED)
            self.set_userinfo(request, user)
            # 登录成功，重新调用自身函数，即可退出
            return self.process_view(request, view, args, kwargs)
        return WebUtils.response_401(_("please provide Token"))
