from apps.knowledge_mgmt.models import KnowledgeDocument


class KnowledgeDocumentUtils(object):
    @staticmethod
    def get_new_document(kwargs, username):
        return KnowledgeDocument.objects.create(
            knowledge_base_id=kwargs["knowledge_base_id"],
            name=kwargs["name"],
            created_by=username,
        )
