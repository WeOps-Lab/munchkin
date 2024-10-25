import hashlib

from django.http import FileResponse, JsonResponse
from django_minio_backend import MinioBackend
from rest_framework.exceptions import NotFound

from apps.bot_mgmt.models import Bot, RasaModel
from apps.bot_mgmt.models.bot import BotChannel
from apps.core.utils.exempt import api_exempt


@api_exempt
def get_bot_detail(request, bot_id):
    channels = BotChannel.objects.filter(bot_id=bot_id)
    return_data = {
        "channels": [
            {
                "id": i.id,
                "name": i.name,
                "channel_type": i.channel_type,
                "channel_config": i.format_channel_config(),
                "enabled": i.enabled,
            }
            for i in channels
        ],
    }
    return JsonResponse(return_data)


@api_exempt
def model_download(request):
    try:
        bot_id = request.GET.get("bot_id")
        rasa_model = Bot.objects.filter(id=bot_id).first().rasa_model
    except RasaModel.DoesNotExist:
        raise NotFound("RasaModel with given id not found")

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
