from typing import List

from django.conf import settings
from django.utils.translation import gettext as _
from langchain_core.documents import Document
from langserve import RemoteRunnable

from apps.knowledge_mgmt.services.knowledge_search_service import KnowledgeSearchService
from apps.model_provider_mgmt.models import LLMModelChoices, LLMSkill


class LLMService:
    def __init__(self):
        self.knowledge_search_service = KnowledgeSearchService()

    def chat(self, llm_skill: LLMSkill, user_message, chat_history, enable_online_search=False):
        llm_model = llm_skill.llm_model

        context = ""
        result = ""
        title_list = set()
        online_search_result = []
        if llm_skill.enable_rag:
            knowledge_base_folder_list = llm_skill.knowledge_base.all()
            for i in knowledge_base_folder_list:
                kwargs = {
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
                    knowledge_base_folder_list, user_message, kwargs, score_threshold=llm_skill.rag_score_threshold
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
        if enable_online_search:
            rag_server = RemoteRunnable(settings.ONLINE_SEARCH_SERVER_URL)
            online_search_result: List[Document] = rag_server.invoke(
                {
                    "query": user_message,
                }
            )
            context += "--------\n"
            context += _("The following are the online search results:") + "\n"
            for r in online_search_result:
                context += _("Title:[{}]\n").format(r.page_content)

        if llm_model.llm_model_type == LLMModelChoices.CHAT_GPT:
            chat_server = RemoteRunnable(settings.OPENAI_CHAT_SERVICE_URL)
            result = chat_server.invoke(
                {
                    "system_message_prompt": llm_skill.skill_prompt,
                    "openai_api_base": llm_model.decrypted_llm_config["openai_base_url"],
                    "openai_api_key": llm_model.decrypted_llm_config["openai_api_key"],
                    "temperature": llm_model.decrypted_llm_config["temperature"],
                    "model": llm_model.decrypted_llm_config["model"],
                    "user_message": user_message,
                    "chat_history": chat_history,
                    "conversation_window_size": llm_skill.conversation_window_size,
                    "rag_context": context,
                }
            )

        if llm_skill.enable_rag_knowledge_source:
            result += "\n"
            result += _("Citing Knowledge: {}").format(", ".join(list(title_list))) + "\n"

        if enable_online_search:
            result += "\n"
            result += _("Website Source:") + "\n"
            for r in online_search_result:
                result += f"* [{r.metadata['title']}]({r.metadata['url']})\n"
        return result


llm_service = LLMService()
