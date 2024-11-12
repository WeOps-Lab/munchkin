import datetime

from django.contrib.postgres.aggregates import ArrayAgg
from django.core.paginator import Paginator
from django.db.models import Count, Max, Min, OuterRef, Subquery
from django.db.models.functions import TruncDay
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.bot_mgmt.models import BotConversationHistory
from apps.bot_mgmt.serializers.history_serializer import HistorySerializer
from apps.channel_mgmt.models import ChannelChoices


class HistoryViewSet(viewsets.ModelViewSet):
    serializer_class = HistorySerializer
    queryset = BotConversationHistory.objects.all()

    @action(methods=["GET"], detail=False)
    def search_log(self, request):
        bot_id, channel_type, end_time, page, page_size, search, start_time = self.set_log_params(request)

        earliest_conversation_subquery = (
            BotConversationHistory.objects.filter(
                bot=OuterRef("bot"), channel_user=OuterRef("channel_user"), created_at__date=OuterRef("day")
            )
            .order_by("created_at")
            .values("conversation")[:1]
        )
        aggregated_data = (
            BotConversationHistory.objects.filter(
                created_at__range=(start_time, end_time),
                bot_id=bot_id,
                channel_user__channel_type__in=channel_type,
                channel_user__name__icontains=search,
            )
            .annotate(day=TruncDay("created_at"))
            .values("day", "channel_user__user_id", "channel_user__name", "channel_user__channel_type")
            .annotate(
                count=Count("id"),
                ids=ArrayAgg("id"),
                earliest_created_at=Min("created_at"),
                last_updated_at=Max("created_at"),
                title=Subquery(earliest_conversation_subquery),
            )
            .order_by("day", "channel_user__user_id")
        )
        paginator, result = self.get_log_by_page(aggregated_data, page, page_size)
        return JsonResponse({"result": True, "data": {"items": result, "count": paginator.count}})

    @staticmethod
    def get_log_by_page(aggregated_data, page, page_size):
        paginator = Paginator(aggregated_data, page_size)
        # 将结果转换为期望的格式
        result = []
        try:
            page_data = paginator.page(page)
        except Exception:
            # 处理无效的页码请求
            page_data = paginator.page(1)  # 返回第一页数据
        for entry in page_data:
            result.append(
                {
                    "sender_id": entry["channel_user__user_id"],
                    "username": entry["channel_user__name"],
                    "channel_type": dict(ChannelChoices.choices).get(
                        entry["channel_user__channel_type"], entry["channel_user__channel_type"]
                    ),
                    "count": entry["count"],
                    "ids": entry["ids"],
                    "created_at": entry["earliest_created_at"].strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "updated_at": entry["last_updated_at"].strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "title": entry["title"],
                }
            )
        return paginator, result

    @staticmethod
    def set_log_params(request):
        start_time_str = request.GET.get("start_time")
        end_time_str = request.GET.get("end_time")
        page_size = int(request.GET.get("page_size", 10))
        page = int(request.GET.get("page", 1))
        bot_id = request.GET.get("bot_id")
        search = request.GET.get("search", "")
        channel_type = request.GET.get("channel_type", "")
        if not channel_type:
            channel_type = list(dict(ChannelChoices.choices).keys())
        else:
            channel_type = channel_type.split(",")
        today = datetime.datetime.today()
        # 解析时间字符串到 datetime 对象，并处理空值
        if start_time_str:
            start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            start_time = today.replace(year=2024, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        if end_time_str:
            end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            end_time = today.replace(hour=23, minute=59, second=59, microsecond=999999)
        return bot_id, channel_type, end_time, page, page_size, search, start_time

    @action(methods=["POST"], detail=False)
    def get_log_detail(self, request):
        ids = request.data.get("ids")
        page_size = int(request.data.get("page_size", 10))
        page = int(request.data.get("page", 1))
        history_list = (
            BotConversationHistory.objects.filter(id__in=ids)
            .values("conversation_role", "conversation")
            .order_by("created_at")
        )
        paginator = Paginator(history_list, page_size)
        # 将结果转换为期望的格式
        try:
            page_data = paginator.page(page)
        except Exception:
            # 处理无效的页码请求
            page_data = paginator.page(1)  # 返回第一页数据
        return_data = []
        for i in page_data:
            return_data.append({"role": i["conversation_role"], "content": i["conversation"]})
        return JsonResponse({"result": True, "data": return_data})
