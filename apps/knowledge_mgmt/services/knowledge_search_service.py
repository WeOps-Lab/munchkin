from typing import List

from django.conf import settings
from langserve import RemoteRunnable

from apps.knowledge_mgmt.remote_service import RAG_SERVER_URL
from apps.model_provider_mgmt.models import EmbedProvider, RerankProvider


class KnowledgeSearchService:
    @staticmethod
    def search(knowledge_base_folder, query, kwargs) -> List[dict]:
        docs = []
        remote_indexer = RemoteRunnable(RAG_SERVER_URL)

        embed_model_address = EmbedProvider.objects.get(id=kwargs["embed_model"]).embed_config["base_url"]
        rerank_model_address = ""

        if kwargs["enable_rerank"]:
            rerank_model_address = RerankProvider.objects.get(id=kwargs["rerank_model"]).rerank_config["base_url"]
        params = {
            "elasticsearch_url": settings.ELASTICSEARCH_URL,
            "elasticsearch_password": settings.ELASTICSEARCH_PASSWORD,
            "embed_model_address": embed_model_address,
            "index_name": knowledge_base_folder.knowledge_index_name(),
            "search_query": query,
            "metadata_filter": {"enabled": True},
            "rag_k": kwargs["rag_k"],  # 返回结果数量
            "rag_num_candidates": kwargs["rag_num_candidates"],  # 候选数量
            "enable_rerank": kwargs["enable_rerank"],
            "rerank_model_address": rerank_model_address,
            "rerank_top_k": 10,  # Rerank返回结果数量
        }
        if kwargs["enable_text_search"]:
            params["text_search_weight"] = kwargs["text_search_weight"]
        if kwargs["enable_vector_search"]:
            params["vector_search_weight"] = kwargs["vector_search_weight"]
        result = remote_indexer.invoke(params)
        for doc in result:
            score = doc.metadata["_score"] * 10
            if not score:
                continue

            doc_info = {
                "content": doc.page_content,
                "score": score,
                "knowledge_id": doc.metadata["_source"]["metadata"]["knowledge_id"],
            }
            if knowledge_base_folder.enable_rerank:
                doc_info["rerank_score"] = doc.metadata["relevance_score"]
            docs.append(doc_info)

        return docs
