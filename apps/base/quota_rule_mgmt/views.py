from django.http import JsonResponse
from django_filters import filters
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.base.models import QuotaRule
from apps.base.quota_rule_mgmt.quota_utils import QuotaUtils
from apps.base.quota_rule_mgmt.serializers import QuotaRuleSerializer
from apps.core.decorators.api_perminssion import HasRole


class ObjFilter(FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")


class QuotaRuleViewSet(viewsets.ModelViewSet):
    queryset = QuotaRule.objects.all()
    serializer_class = QuotaRuleSerializer
    ordering = ("-id",)
    filterset_class = ObjFilter

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
        current_team = request.COOKIES.get("current_team")
        if not current_team:
            current_team = teams[0]
        client = QuotaUtils(username, current_team)
        all_file_size, used_file_size = client.get_file_quota()
        skill_count, used_skill_count = client.get_skill_quota()
        bot_count, used_bot_count = client.get_bot_quota()

        return_data = {
            "used_file_size": used_file_size,
            "used_skill_count": used_skill_count,
            "used_bot_count": used_bot_count,
            "all_file_size": all_file_size,
            "all_skill_count": skill_count,
            "all_bot_count": bot_count,
        }
        return JsonResponse({"result": True, "data": return_data})
