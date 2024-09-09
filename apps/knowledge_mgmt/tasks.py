from celery import shared_task


@shared_task
def general_embed(knowledge_document_id_list, source_type):
    from apps.knowledge_mgmt.knowledge_document_mgmt.utils import KnowledgeDocumentUtils

    KnowledgeDocumentUtils.general_embed_by_document_list(knowledge_document_id_list, source_type)
