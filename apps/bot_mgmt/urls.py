from django.urls import path
from rest_framework import routers

from apps.bot_mgmt import views
from apps.bot_mgmt.viewsets import BotViewSet, RasaModelViewSet
from apps.bot_mgmt.viewsets.history_view import HistoryViewSet

router = routers.DefaultRouter()
router.register(r"bot", BotViewSet)
router.register(r"rasa_model", RasaModelViewSet, basename="rasa_model")
router.register(r"history", HistoryViewSet)
urlpatterns = router.urls

urlpatterns += [
    path(r"bot/<int:bot_id>/get_detail/", views.get_bot_detail, name="get_bot_detail"),
    path(r"rasa_model_download/", views.model_download, name="model_download"),
    path(r"skill_execute/", views.skill_execute, name="skill_execute"),
    # path(r"api/bot/automation_skill_execute", AutomationSkillExecuteView.as_view(), name="automation_skill_execute"),
]
