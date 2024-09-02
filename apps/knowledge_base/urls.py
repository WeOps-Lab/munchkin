from django.contrib import admin
from rest_framework import routers

from apps.knowledge_base.knowledge_base_mgmt.views import KnowledgeBaseViewSet
from apps.knowledge_base.knowledge_document_mgmt.views import KnowledgeDocumentViewSet

admin.site.site_title = "Knowledge Base"
admin.site.site_header = admin.site.site_title
router = routers.DefaultRouter()
router.register(r"knowledge_base", KnowledgeBaseViewSet)
router.register(r"knowledge_document", KnowledgeDocumentViewSet)

urlpatterns = router.urls
