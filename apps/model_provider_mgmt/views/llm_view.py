from django.http import JsonResponse
from rest_framework.decorators import action

from apps.core.decorators.api_perminssion import HasRole
from apps.core.viewsets.guardian_model_viewset import GuardianModelViewSet
from apps.knowledge_mgmt.viewset_utils import AuthViewSet
from apps.model_provider_mgmt.models import LLMModel, LLMSkill
from apps.model_provider_mgmt.serializers.llm_serializer import LLMModelSerializer, LLMSerializer
from apps.model_provider_mgmt.services.llm_service import llm_service


class LLMViewSet(AuthViewSet):
    serializer_class = LLMSerializer
    queryset = LLMSkill.objects.all()
    search_fields = ["name"]

    @HasRole()
    def list(self, request, *args, **kwargs):
        name = request.query_params.get("name", "")
        queryset = LLMSkill.objects.filter(name__icontains=name)
        return self.query_by_groups(request, queryset, "groups")

    @action(methods=["POST"], detail=False)
    @HasRole()
    def execute(self, request):
        """
        {
            "user_message": "你好", # 用户消息
            "llm_model": 1, # 大模型ID
            "skill_prompt": "abc", # Prompt
            "enable_rag": True, # 是否启用RAG
            "enable_rag_knowledge_source": True, # 是否显示RAG知识来源
            "knowledge_base": [1], # 知识库ID列表
            "rag_score_threshold": 0.7, # RAG分数阈值
            "chat_history": "abc", # 对话历史
            "conversation_window_size": 10 # 对话窗口大小
        }
        """
        params = request.data
        result = llm_service.chat(params)
        return JsonResponse({"result": result})


class LLMModelViewSet(GuardianModelViewSet):
    serializer_class = LLMModelSerializer
    queryset = LLMModel.objects.all()
    search_fields = ["name"]
