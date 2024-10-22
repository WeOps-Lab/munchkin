from django.http import JsonResponse
from django.utils.translation import gettext as _
from rest_framework.decorators import action

from apps.bot_mgmt.models import Bot
from apps.bot_mgmt.serializers import BotSerializer
from apps.channel_mgmt.models import Channel
from apps.core.decorators.api_perminssion import HasRole
from apps.core.utils.kubernetes_client import KubernetesClient
from apps.core.utils.viewset_utils import AuthViewSet
from apps.model_provider_mgmt.models import LLMSkill


class BotViewSet(AuthViewSet):
    serializer_class = BotSerializer
    queryset = Bot.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        Bot.objects.create(name=data.get("name"), introduction=data.get("introduction"), team=data.get("team"))
        return JsonResponse({"result": True})

    def update(self, request, *args, **kwargs):
        data = request.data
        is_publish = data.pop("is_publish", False)
        obj: Bot = self.get_object()
        channels = data.pop("channels", [])
        llm_skills = data.pop("llm_skills", [])
        rasa_model = data.pop("rasa_model", None)
        for key in data.keys():
            setattr(obj, key, data[key])
        if rasa_model is not None:
            obj.rasa_model_id = rasa_model
        if channels:
            obj.channels.set(Channel.objects.filter(id__in=channels))
        if llm_skills:
            obj.llm_skills.set(LLMSkill.objects.filter(id__in=llm_skills))
        obj.online = is_publish
        obj.save()
        if is_publish:
            client = KubernetesClient()
            client.start_pilot(obj)
        return JsonResponse({"result": True})

    def destroy(self, request, *args, **kwargs):
        obj: Bot = self.get_object()
        if obj.online:
            return JsonResponse({"result": False, "message": _("Please stop the bot first.")})
        return super().destroy(request, *args, **kwargs)

    @HasRole()
    def list(self, request, *args, **kwargs):
        name = request.query_params.get("name", "")
        queryset = Bot.objects.filter(name__icontains=name)
        return self.query_by_groups(request, queryset)

    @action(methods=["POST"], detail=False)
    def start_pilot(self, request):
        bot_ids = request.data.get("bot_ids")
        bots = Bot.objects.filter(id__in=bot_ids)
        client = KubernetesClient()
        for bot in bots:
            client.start_pilot(bot)
            bot.online = True
            bot.save()
        return JsonResponse({"result": True})

    @action(methods=["POST"], detail=False)
    def stop_pilot(self, request):
        bot_ids = request.data.get("bot_ids")
        bots = Bot.objects.filter(id__in=bot_ids)
        client = KubernetesClient()
        for bot in bots:
            client.stop_pilot(bot.id)
            bot.online = False
            bot.save()
        return JsonResponse({"result": True})