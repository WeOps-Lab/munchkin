from typing import Dict

from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_elasticsearch import ElasticsearchRetriever
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.embed_mgmt.models import EmbedModelChoices
from apps.knowledge_mgmt.models import KnowledgeBaseFolder
from munchkin.components.elasticsearch import ELASTICSEARCH_URL


class RagSearchView(APIView):

    def vector_query(self, search_query: str, embeddings, k, num_candidates) -> Dict:
        vector = embeddings.embed_query(search_query)
        return {
            "query": {
                "match": {
                    'text': search_query,
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
            }
        }

    @swagger_auto_schema(
        operation_id="rag_search",
        operation_description="知识检索",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "ids": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER)),
                "query": openapi.Schema(type=openapi.TYPE_STRING, description="查询内容"),
                "k": openapi.Schema(type=openapi.TYPE_INTEGER, description="返回结果数量", default=10),
                "num_candidates": openapi.Schema(type=openapi.TYPE_INTEGER, description="候选数量", default=10),
                "enable_vector_search": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="是否启用向量检索"),
                "enable_text_search": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="是否启用文本检索"),
            },
            required=["ids", "query"],
        ),
    )
    def post(self, request, format=None):
        context = []

        for i in request.data.get('ids'):
            try:
                knowledge_base_folder = KnowledgeBaseFolder.objects.get(id=i)
            except KnowledgeBaseFolder.DoesNotExist:
                continue

            if knowledge_base_folder.embed_model.enbed_model == EmbedModelChoices.FASTEMBED:
                model_configs = knowledge_base_folder.embed_model.embed_config
                embedding = FastEmbedEmbeddings(model_name=model_configs['model'], cache_dir='models')

            index_name = f"knowledge_base_{knowledge_base_folder.id}"
            vector_retriever = ElasticsearchRetriever.from_es_params(
                index_name=index_name,
                body_func=lambda x: self.vector_query(x, embedding,
                                                      request.data.get('k', 10),
                                                      request.data.get('num_candidates', 10)),
                content_field='text',
                url=ELASTICSEARCH_URL,
            )
            result = vector_retriever.invoke(request.data.get('query'))
            for r in result:
                context.append(r.page_content)
        return Response({"context": context})
