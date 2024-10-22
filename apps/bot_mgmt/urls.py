# from django.urls import path
from rest_framework import routers

from apps.bot_mgmt.views import BotViewSet, RasaModelViewSet

router = routers.DefaultRouter()
router.register(r"bot", BotViewSet)
router.register(r"rasa_model", RasaModelViewSet, basename="rasa_model")
urlpatterns = router.urls

# urlpatterns += [
#     path(r"api/bot/skill_execute", SkillExecuteView.as_view(), name="skill_execute"),
#     path(r"api/bot/automation_skill_execute", AutomationSkillExecuteView.as_view(), name="automation_skill_execute"),
# ]
