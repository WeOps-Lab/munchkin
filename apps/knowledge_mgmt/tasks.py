from celery import shared_task

from apps.knowledge_mgmt.models import KnowledgeDocument


@shared_task
def general_embed(knowledge_document_id_list):
    from apps.knowledge_mgmt.knowledge_document_mgmt.utils import KnowledgeDocumentUtils

    document_list = KnowledgeDocument.objects.filter(id__in=knowledge_document_id_list)
    KnowledgeDocumentUtils.general_embed_by_document_list(document_list)


@shared_task
def retrain_all(knowledge_base_id):
    from apps.knowledge_mgmt.knowledge_document_mgmt.utils import KnowledgeDocumentUtils

    document_list = KnowledgeDocument.objects.filter(knowledge_base_id=knowledge_base_id)
    KnowledgeDocumentUtils.general_embed_by_document_list(document_list)
