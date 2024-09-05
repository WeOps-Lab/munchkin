from rest_framework import routers

from apps.model_provider_mgmt.views.embed_view import EmbedProviderViewSet, EmbedViewSet
from apps.model_provider_mgmt.views.llm_view import LLMViewSet
from apps.model_provider_mgmt.views.ocr_view import OCRProviderViewSet
from apps.model_provider_mgmt.views.rerank_view import RerankProviderViewSet, RerankViewSet

router = routers.DefaultRouter()
router.register(r"embed", EmbedViewSet, basename="embed")
router.register(r"embed_provider", EmbedProviderViewSet)
router.register(r"rerank_provider", RerankProviderViewSet)
router.register(r"ocr_provider", OCRProviderViewSet)
router.register(r"rerank", RerankViewSet, basename="rerank")
router.register(r"llm", LLMViewSet, basename="llm")
urlpatterns = router.urls
