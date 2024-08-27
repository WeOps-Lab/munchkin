from rest_framework import routers

from apps.base.views import UserAPISecretViewSet

router = routers.DefaultRouter()
urlpatterns = []
router.register(r"user_api_secret", UserAPISecretViewSet)

urlpatterns += router.urls
