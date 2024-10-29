import hashlib

from django.http import FileResponse, JsonResponse
from django_minio_backend import MinioBackend

from apps.bot_mgmt.models import Bot
from apps.bot_mgmt.models.bot import BotChannel
from apps.bot_mgmt.services.skill_excute_service import SkillExecuteService
from apps.core.utils.exempt import api_exempt


@api_exempt
def get_bot_detail(request, bot_id):
    api_token = request.META.get("HTTP_AUTHORIZATION")
    if not api_token:
        return JsonResponse({})
    bot = Bot.objects.filter(id=bot_id, api_token=api_token).first()
    if not bot:
        return JsonResponse({})
    channels = BotChannel.objects.filter(bot_id=bot_id, enabled=True)
    return_data = {
        "channels": [
            {
                "id": i.id,
                "name": i.name,
                "channel_type": i.channel_type,
                "channel_config": i.format_channel_config(),
            }
            for i in channels
        ],
    }
    return JsonResponse(return_data)


@api_exempt
def model_download(request):
    bot_id = request.GET.get("bot_id")
    api_token = request.META.get("HTTP_AUTHORIZATION")
    if not api_token:
        return JsonResponse({})
    bot = Bot.objects.filter(id=bot_id, api_token=api_token).first()
    if not bot:
        return JsonResponse({})
    rasa_model = bot.rasa_model
    if not rasa_model:
        return JsonResponse({})
    storage = MinioBackend(bucket_name="munchkin-private")
    file = storage.open(rasa_model.model_file.name, "rb")

    # Calculate ETag
    data = file.read()
    etag = hashlib.md5(data).hexdigest()

    # Reset file pointer to start
    file.seek(0)

    response = FileResponse(file)
    response["ETag"] = etag

    return response


@api_exempt
def skill_execute(request):
    skill_id = request.data.get("skill_id")
    user_message = request.data.get("user_message")
    sender_id = request.data.get("sender_id", "")
    chat_history = request.data.get("chat_history", [])
    bot_id = request.GET.get("bot_id")
    api_token = request.META.get("HTTP_AUTHORIZATION")
    if not api_token:
        return JsonResponse({"result": "No authorization"})
    bot = Bot.objects.filter(id=bot_id, api_token=api_token).first()
    if not bot:
        return JsonResponse({"result": "No bot found"})
    result = SkillExecuteService.execute_skill(bot_id, skill_id, user_message, chat_history, sender_id)

    return JsonResponse({"result": result})
