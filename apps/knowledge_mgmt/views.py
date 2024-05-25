from typing import Dict

import tiktoken
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_elasticsearch import ElasticsearchRetriever
from loguru import logger
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.llm_mgmt.models import EmbedModelChoices
from apps.knowledge_mgmt.models import KnowledgeBaseFolder
from apps.knowledge_mgmt.services import RagService
from munchkin.components.elasticsearch import ELASTICSEARCH_URL


class RagSearchView(APIView):

    @swagger_auto_schema(
        operation_id="rag_search",
        operation_description="知识检索",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "ids": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER)),
                "query": openapi.Schema(type=openapi.TYPE_STRING, description="查询内容"),
                "k": openapi.Schema(type=openapi.TYPE_INTEGER, description="返回结果数量", default=5),
                "num_candidates": openapi.Schema(type=openapi.TYPE_INTEGER, description="候选数量", default=1000),
                "enable_vector_search": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="是否启用向量检索"),
                "enable_text_search": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="是否启用文本检索"),
            },
            required=["ids", "query"],
        ),
    )
    def post(self, request, format=None):
        context = RagService().rag_serch(ids=request.data.get('ids'),
                                         k=request.data.get('k', 5),
                                         num_candidates=request.data.get('num_candidates', 1000),
                                         user_message=request.data.get('query'))
        return Response({"context": context})
