from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.core.viewsets.guardian_model_viewset import GuardianModelViewSet
from apps.model_provider_mgmt.models import LLMModel, LLMSkill
from apps.model_provider_mgmt.serializers.llm_serializer import LLMModelSerializer
from apps.model_provider_mgmt.services.llm_service import llm_service


class LLMViewSet(viewsets.ViewSet):
    @action(methods=["post"], detail=False)
    def execute(self, request):
        user_message = request.data.get("user_message")
        chat_history = request.data.get("chat_history")
        super_system_prompt = request.data.get("super_system_prompt", None)

        llm_skill_id = request.data.get("llm_skill_id")
        llm_skill = LLMSkill.objects.get(id=llm_skill_id)
        if super_system_prompt:
            llm_skill.skill_prompt = super_system_prompt
        result = llm_service.chat(llm_skill, user_message, chat_history)
        return JsonResponse({"result": result})


class LLMModelViewSet(GuardianModelViewSet):
    serializer_class = LLMModelSerializer
    queryset = LLMModel.objects.all()
    search_fields = ["name"]
