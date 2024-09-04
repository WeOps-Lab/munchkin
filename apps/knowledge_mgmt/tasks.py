from celery import shared_task
from django.conf import settings
from django.utils.translation import gettext as _
from dotenv import load_dotenv
from langserve import RemoteRunnable
from tqdm import tqdm

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
    from apps.model_provider_mgmt.models import EmbedProvider, OCRProvider

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
    embed_provider_map = dict(EmbedProvider.objects.filter(enabled=True).values_list("id", "embed_config"))
    ocr_provider_map = dict(OCRProvider.objects.filter(enabled=True).values_list("id", "ocr_config"))

    knowledge_docs = invoke_remote(source_remote, source_type, document_list, embed_provider_map, ocr_provider_map)
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


def invoke_remote(source_remote, source_type, document_list, embed_provider_map, ocr_provider_map):
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
        kwargs = format_invoke_kwargs(document, embed_provider_map, ocr_provider_map)
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


def format_invoke_kwargs(knowledge_document: KnowledgeDocument, embed_provider_map, ocr_provider_map):
    semantic_embedding_address = []
    for i in knowledge_document.semantic_chunk_parse_embedding_model:
        if embed_provider_map.get(int(i)):
            semantic_embedding_address.append(embed_provider_map[int(i)]["base_url"])
    if not semantic_embedding_address:
        semantic_embedding_address = ""
    ocr_provider_address = []
    for i in knowledge_document.ocr_model:
        if ocr_provider_map.get(int(i)):
            ocr_provider_address.append(ocr_provider_map[int(i)]["base_url"])
    if not ocr_provider_address:
        ocr_provider_address = ""
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


@shared_task
def general_embed(knowledge_document_id):
    file_remote = RemoteRunnable(FILE_CHUNK_SERIVCE_URL)
    manual_remote = RemoteRunnable(MANUAL_CHUNK_SERVICE_URL)
    web_page_remote = RemoteRunnable(WEB_PAGE_CHUNK_SERVICE_URL)
    remote_indexer = RemoteRunnable(REMOTE_INDEX_URL)
    knowledge_document = KnowledgeDocument.objects.get(id=knowledge_document_id)
    knowledge_base_folder = knowledge_document.knowledge_base
    index_name = knowledge_base_folder.knowledge_index_name()
    knowledge_base_folder_id = knowledge_base_folder.id
    try:
        knowledge_document.train_status = 1
        knowledge_document.train_progress = 0
        knowledge_document.save()
        knowledge_list = []
        file_knowledges = FileKnowledge.objects.filter(knowledge_document_id=knowledge_document_id).all()
        logger.info(f"知识库[{knowledge_base_folder.id}]包含[{len(file_knowledges)}]个文件知识")
        for obj in file_knowledges:
            knowledge_list.append(obj)
        manual_knowledges = ManualKnowledge.objects.filter(knowledge_base_folder=knowledge_base_folder).all()
        logger.info(f"知识库[{knowledge_base_folder.id}]包含[{len(manual_knowledges)}]个手动知识")
        for obj in manual_knowledges:
            knowledge_list.append(obj)
        web_page_knowledges = WebPageKnowledge.objects.filter(knowledge_base_folder=knowledge_base_folder).all()
        logger.info(f"知识库[{knowledge_base_folder.id}]包含[{len(web_page_knowledges)}]个网页知识")
        for obj in web_page_knowledges:
            knowledge_list.append(obj)
        total_knowledges = len(knowledge_list)
        knowledge_docs = []
        for index, knowledge in tqdm(enumerate(knowledge_list)):
            semantic_embedding_address = ""

            semantic_chunk_parse_embedding_model = knowledge.semantic_chunk_parse_embedding_model
            if semantic_chunk_parse_embedding_model is not None:
                semantic_embedding_address = semantic_chunk_parse_embedding_model.embed_config["base_url"]

            ocr_provider_address = ""
            if knowledge_base_folder.ocr_model is not None:
                ocr_provider_address = knowledge_base_folder.ocr_model.ocr_config["base_url"]
            kwargs = {
                "enable_recursive_chunk_parse": knowledge.knowledge_document.enable_general_parse,
                "recursive_chunk_size": knowledge.knowledge_document.general_parse_chunk_size,
                "recursive_chunk_overlap": knowledge.knowledge_document.general_parse_chunk_overlap,
                "enable_semantic_chunk_parse": knowledge.knowledge_document.enable_semantic_chunk_parse,
                "enable_ocr_parse": knowledge.knowledge_document.enable_ocr_parse,
                "semantic_embedding_address": semantic_embedding_address,
                "excel_header_row_parse": knowledge.knowledge_document.excel_header_row_parse,
                "excel_full_content_parse": knowledge.knowledge_document.excel_full_content_parse,
                "ocr_provider_address": ocr_provider_address,
                "custom_metadata": {
                    "knowledge_type": "file",
                    "knowledge_id": knowledge.id,
                    "knowledge_title": knowledge.knowledge_document.name,
                    "knowledge_folder_id": knowledge.knowledge_document.knowledge_base.id,
                },
            }
            if isinstance(knowledge, FileKnowledge):
                logger.debug(f"开始处理文件知识: {knowledge.knowledge_document.name}")

                remote_docs = file_remote.invoke(
                    dict(
                        kwargs,
                        **{
                            "file_name": knowledge.file.name,
                            "file": knowledge.get_file_base64(),
                        },
                    )
                )
                knowledge_docs.extend(remote_docs)
                logger.info(f"文件知识[{knowledge.knowledge_document.name}]共提取[{len(remote_docs)}]个文档片段")
            elif isinstance(knowledge, ManualKnowledge):
                logger.debug(f"开始处理手动知识: {knowledge.knowledge_document.name}")
                remote_docs = manual_remote.invoke(
                    dict(
                        kwargs,
                        **{
                            "content": knowledge.knowledge_document.name + knowledge.content,
                        },
                    )
                )
                knowledge_docs.extend(remote_docs)
                logger.info(f"手动知识[{knowledge.knowledge_document.name}]共提取[{len(remote_docs)}]个文档片段")
            elif isinstance(knowledge, WebPageKnowledge):
                logger.debug(f"开始处理网页知识: {knowledge.knowledge_document.name}")
                remote_docs = web_page_remote.invoke(
                    dict(
                        kwargs,
                        **{
                            "url": knowledge.url,
                            "max_depth": knowledge.max_depth,
                        },
                    )
                )
                knowledge_docs.extend(remote_docs)
                logger.info(f"网页知识[{knowledge.knowledge_document.name}]共提取[{len(remote_docs)}]个文档片段")
            progress = round((index + 1) / total_knowledges * 100, 2)
            logger.debug(f"知识库[{knowledge_base_folder_id}]的Embedding索引生成进度: {progress:.2f}%")
            knowledge_document.train_progress = progress
            knowledge_document.save()
        logger.debug(f"开始写入知识库[{knowledge_base_folder_id}]")
        remote_indexer.invoke(
            {
                "elasticsearch_url": settings.ELASTICSEARCH_URL,
                "elasticsearch_password": settings.ELASTICSEARCH_PASSWORD,
                "embed_model_address": knowledge_base_folder.embed_model.embed_config["base_url"],
                "index_name": index_name,
                "index_mode": "overwrite",
                "docs": knowledge_docs,
            }
        )

        knowledge_document.train_status = 2
        knowledge_document.train_progress = 100
        knowledge_document.save()
    except Exception as e:
        logger.exception(e)
        knowledge_document.train_status = 3
        knowledge_document.train_progress = 100
        knowledge_document.save()


def file_knowledge_embed(knowledge_id):
    pass
