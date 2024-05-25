from django.urls import path
from rest_framework import routers

from apps.bot_mgmt.views import SkillExecuteView

router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path(r'api/bot/skill_execute', SkillExecuteView.as_view(), name='skill_execute'),
]
