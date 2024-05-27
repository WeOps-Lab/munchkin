from django.urls import path
from rest_framework import routers

from apps.contentpack_mgmt.views import ModelDownloadView

router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path(r'api/contentpack/model_download', ModelDownloadView.as_view(), name='model_download'),
]
