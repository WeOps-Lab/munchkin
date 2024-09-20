from apps.knowledge_mgmt.models import KnowledgeDocument
from apps.knowledge_mgmt.models.knowledge_document import DocumentStatus


class KnowledgeDocumentUtils(object):
    @staticmethod
    def get_new_document(kwargs, username):
        return KnowledgeDocument.objects.create(
            knowledge_base_id=kwargs["knowledge_base_id"],
            name=kwargs["name"],
            knowledge_source_type=kwargs["knowledge_source_type"],
            created_by=username,
            train_status=DocumentStatus.PENDING,
        )
