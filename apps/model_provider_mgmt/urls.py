from rest_framework import routers

from apps.model_provider_mgmt.views.embed_view import EmbedProviderViewSet, EmbedViewSet
from apps.model_provider_mgmt.views.llm_view import LLMViewSet
from apps.model_provider_mgmt.views.rerank_view import RerankViewSet

router = routers.DefaultRouter()
router.register(r"api/embed", EmbedViewSet, basename="embed")
router.register(r"api/embed_provider", EmbedProviderViewSet, basename="embed_provider")
router.register(r"api/rerank", RerankViewSet, basename="rerank")
router.register(r"api/llm", LLMViewSet, basename="llm")
urlpatterns = router.urls
