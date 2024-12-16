from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.base.models import QuotaRule
from apps.base.quota_rule_mgmt.quota_utils import QuotaUtils
from apps.base.quota_rule_mgmt.serializers import QuotaRuleSerializer
from apps.core.decorators.api_perminssion import HasRole


class QuotaRuleViewSet(viewsets.ModelViewSet):
    queryset = QuotaRule.objects.all()
    serializer_class = QuotaRuleSerializer
    ordering = ("-id",)

    @HasRole("admin")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @HasRole("admin")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @HasRole("admin")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @HasRole("admin")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["GET"])
    def my_quota(self, request):
        username = request.user.username
        teams = request.user.group_list
        client = QuotaUtils(username, teams)
        file_size_list = client.get_file_quota()
        skill_count_list = client.get_skill_quota()
        bot_count_list = client.get_bot_quota()
        return_data = {
            "file_size": min(file_size_list) if file_size_list else 0,
            "skill_count": min(skill_count_list) if skill_count_list else 0,
            "bot_count": min(bot_count_list) if bot_count_list else 0,
        }
        return JsonResponse({"result": True, "data": return_data})
