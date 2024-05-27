from django.http import FileResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from django_minio_backend import MinioBackend
from apps.contentpack_mgmt.models import RasaModel
import hashlib


class ModelDownloadView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Download a RasaModel file",
        responses={200: openapi.Response(description="File downloaded successfully")}
    )
    def get(self, request, format=None):
        try:
            rasa_model = RasaModel.objects.get(id=request.query_params.get('model_id'))
        except RasaModel.DoesNotExist:
            raise NotFound("RasaModel with given id not found")

        storage = MinioBackend(bucket_name='munchkin-private')
        file = storage.open(rasa_model.model_file.name, 'rb')

        # Calculate ETag
        data = file.read()
        etag = hashlib.md5(data).hexdigest()

        # Reset file pointer to start
        file.seek(0)

        response = FileResponse(file)
        response["ETag"] = etag

        return response
