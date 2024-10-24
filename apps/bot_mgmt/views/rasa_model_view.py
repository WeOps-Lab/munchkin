import hashlib

from django.http import FileResponse
from django_minio_backend import MinioBackend
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet

from apps.bot_mgmt.models import Bot, RasaModel
from apps.bot_mgmt.serializers.rasa_model_serializer import RasaModelSerializer


class RasaModelViewSet(ModelViewSet):
    serializer_class = RasaModelSerializer
    queryset = RasaModel.objects.all()

    @action(methods=["GET"], detail=False)
    def model_download(self, request):
        try:
            bot_id = request.query_params.get("bot_id")
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
