from django.contrib import admin
from rest_framework import routers

admin.site.site_title = "Knowledge Base"
admin.site.site_header = admin.site.site_title
router = routers.DefaultRouter()

urlpatterns = router.urls
