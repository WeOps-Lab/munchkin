from django.conf import settings
from django.utils.translation import gettext as _
from langserve import RemoteRunnable

from apps.knowledge_mgmt.models import KnowledgeBase
from apps.knowledge_mgmt.services.knowledge_search_service import KnowledgeSearchService
from apps.model_provider_mgmt.models import LLMModel


class LLMService:
    def __init__(self):
        self.knowledge_search_service = KnowledgeSearchService()

    def chat(self, kwargs: dict):
        llm_model = LLMModel.objects.get(id=kwargs["llm_model"])
        context = ""
        title_list = set()
        if kwargs["enable_rag"]:
            knowledge_base_list = KnowledgeBase.objects.filter(id__in=kwargs["knowledge_base"])
            for i in knowledge_base_list:
                params = {
                    "enable_rerank": i.enable_rerank,
                    "embed_model": i.embed_model.id,
                    "rerank_model": i.rerank_model_id,
                    "rag_k": i.rag_k,
                    "rag_num_candidates": i.rag_num_candidates,
                    "enable_text_search": i.enable_text_search,
                    "text_search_weight": i.text_search_weight,
                    "enable_vector_search": i.enable_vector_search,
                    "vector_search_weight": i.vector_search_weight,
                }
                rag_result = self.knowledge_search_service.search(
                    knowledge_base_list, kwargs["user_message"], params, score_threshold=kwargs["rag_score_threshold"]
                )
                context += _(
                    """
The following is the background knowledge provided to you. The format of the background knowledge is as follows:
--------
Knowledge Title: [Title]
Knowledge Content: [Content]
--------

                 """
                )
                for r in rag_result:
                    context += "--------\n"
                    context += f"Knowledge Title:[{r['knowledge_title']}\n"
                    context += f"Knowledge Content:[{r['content'].replace('{', '').replace('}', '')}]\n"
                    title_list.add(f"Knowledge Base[{i.name}]--{r['knowledge_title']}")
        chat_server = RemoteRunnable(settings.OPENAI_CHAT_SERVICE_URL)
        result = chat_server.invoke(
            {
                "system_message_prompt": kwargs["skill_prompt"],
                "openai_api_base": llm_model.decrypted_llm_config["openai_base_url"],
                "openai_api_key": llm_model.decrypted_llm_config["openai_api_key"],
                "temperature": llm_model.decrypted_llm_config["temperature"],
                "model": llm_model.decrypted_llm_config["model"],
                "user_message": kwargs["user_message"],
                "chat_history": kwargs["chat_history"],
                "conversation_window_size": kwargs["conversation_window_size"],
                "rag_context": context,
            }
        )
        if kwargs["enable_rag_knowledge_source"]:
            result += "\n"
            result += _("Citing Knowledge: {}").format(", ".join(list(title_list))) + "\n"
        return result


llm_service = LLMService()
