from typing import Dict

from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_elasticsearch import ElasticsearchRetriever

from apps.model_provider_mgmt.models import EmbedModelChoices
from apps.knowledge_mgmt.models import KnowledgeBaseFolder
from munchkin.components.elasticsearch import ELASTICSEARCH_URL


class RagService:
    def rag_serch(self, ids, k, num_candidates, user_message):
        context = []

        for i in ids:
            try:
                knowledge_base_folder = KnowledgeBaseFolder.objects.get(id=i)
            except KnowledgeBaseFolder.DoesNotExist:
                continue

            if knowledge_base_folder.embed_model.embed_model == EmbedModelChoices.FASTEMBED:
                model_configs = knowledge_base_folder.embed_model.embed_config
                embedding = FastEmbedEmbeddings(model_name=model_configs['model'], cache_dir='models')

            index_name = f"knowledge_base_{knowledge_base_folder.id}"
            vector_retriever = ElasticsearchRetriever.from_es_params(
                index_name=index_name,
                body_func=lambda x: self.vector_query(x, embedding,
                                                      k, num_candidates),
                content_field='text',
                url=ELASTICSEARCH_URL,
            )
            result = vector_retriever.invoke(user_message)

            for r in result:
                context.append(r.page_content)
        return context

    def vector_query(self, search_query: str, embeddings, k, num_candidates) -> Dict:
        vector = embeddings.embed_query(search_query)
        return {
            "query": {
                "match": {
                    'text': {
                        "query": search_query,
                        "boost": 0.9
                    }
                },
            },
            "knn": {
                "field": 'vector',
                "query_vector": vector,
                "k": k,
                "num_candidates": num_candidates,
                "filter": {
                    "term": {
                        "text": "knowledge_base",
                    },
                },
                "boost": 0.1
            }
        }
