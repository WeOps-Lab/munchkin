from celery import shared_task
from django.conf import settings
from django.utils.translation import gettext as _
from dotenv import load_dotenv
from langserve import RemoteRunnable

from apps.core.logger import celery_logger as logger
from apps.knowledge_mgmt.models import (
    FileKnowledge,
    KnowledgeBase,
    KnowledgeDocument,
    ManualKnowledge,
    WebPageKnowledge,
)
from apps.knowledge_mgmt.remote_service import (
    FILE_CHUNK_SERIVCE_URL,
    MANUAL_CHUNK_SERVICE_URL,
    REMOTE_INDEX_URL,
    WEB_PAGE_CHUNK_SERVICE_URL,
)

load_dotenv()


@shared_task
def general_embed_by_document_list(knowledge_base_id, knowledge_document_id_list, source_type):
    remote_url_map = {
        "file": FILE_CHUNK_SERIVCE_URL,
        "manual": MANUAL_CHUNK_SERVICE_URL,
        "web_page": WEB_PAGE_CHUNK_SERVICE_URL,
    }
    if source_type not in remote_url_map:
        logger.info(f"source_type [{source_type}] is not supported")
        return
    source_remote = RemoteRunnable(remote_url_map[source_type])
    remote_indexer = RemoteRunnable(REMOTE_INDEX_URL)
    knowledge_base = KnowledgeBase.objects.get(id=knowledge_base_id)
    document_list = KnowledgeDocument.objects.filter(id__in=knowledge_document_id_list)
    knowledge_docs = invoke_remote(source_remote, source_type, document_list)
    remote_indexer.invoke(
        {
            "elasticsearch_url": settings.ELASTICSEARCH_URL,
            "elasticsearch_password": settings.ELASTICSEARCH_PASSWORD,
            "embed_model_address": knowledge_base.embed_model.embed_config["base_url"],
            "index_name": knowledge_base.knowledge_index_name(),
            "index_mode": "overwrite",
            "docs": knowledge_docs,
        }
    )


def invoke_remote(source_remote, source_type, document_list):
    knowledge_docs = []
    source_invoke_format_map = {
        "file": format_file_invoke_kwargs,
        "manual": format_manual_invoke_kwargs,
        "web_page": format_web_page_invoke_kwargs,
    }
    for document in document_list:
        document.train_status = 1
        document.train_progress = 0
        document.save()
        logger.debug(_("Start handle {} knowledge: {}").format(source_type, document.name))
        kwargs = format_invoke_kwargs(document)
        kwargs.update(source_invoke_format_map[source_type](document))
        try:
            remote_docs = source_remote.invoke(kwargs)
            knowledge_docs.extend(remote_docs)
            document.train_status = 2
        except Exception as e:
            logger.exception(e)
            document.train_status = 3
        document.train_progress = 100
        document.save()
    return knowledge_docs


def format_file_invoke_kwargs(document):
    knowledge = FileKnowledge.objects.filter(knowledge_document_id=document.id).first()
    return {
        "file_name": document.name,
        "file": knowledge.get_file_base64(),
    }


def format_manual_invoke_kwargs(document):
    knowledge = ManualKnowledge.objects.filter(knowledge_document_id=document.id).first()
    return {
        "content": document.name + knowledge.content,
    }


def format_web_page_invoke_kwargs(document):
    knowledge = WebPageKnowledge.objects.filter(knowledge_document_id=document.id).first()
    return {
        "url": knowledge.url,
        "max_depth": knowledge.max_depth,
    }


def format_invoke_kwargs(knowledge_document: KnowledgeDocument):
    semantic_embedding_address = ""
    if not knowledge_document.semantic_chunk_parse_embedding_model:
        semantic_embedding_address = knowledge_document.semantic_chunk_parse_embedding_model.embed_config["base_url"]
    ocr_provider_address = ""
    if not knowledge_document.ocr_model:
        ocr_provider_address = knowledge_document.ocr_model.ocr_config["base_url"]
    return {
        "enable_recursive_chunk_parse": knowledge_document.enable_general_parse,
        "recursive_chunk_size": knowledge_document.general_parse_chunk_size,
        "recursive_chunk_overlap": knowledge_document.general_parse_chunk_overlap,
        "enable_semantic_chunk_parse": knowledge_document.enable_semantic_chunk_parse,
        "enable_ocr_parse": knowledge_document.enable_ocr_parse,
        "semantic_embedding_address": semantic_embedding_address,
        "excel_header_row_parse": knowledge_document.excel_header_row_parse,
        "excel_full_content_parse": knowledge_document.excel_full_content_parse,
        "ocr_provider_address": ocr_provider_address,
        "custom_metadata": {
            "knowledge_type": "file",
            "knowledge_id": knowledge_document.id,
            "knowledge_title": knowledge_document.name,
            "knowledge_folder_id": knowledge_document.knowledge_base.id,
        },
    }
