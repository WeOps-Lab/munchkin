from rest_framework import viewsets

from apps.base.models import UserAPISecret
from apps.base.user_api_secret_mgmt.serializers import UserAPISecretSerializer


class UserAPISecretViewSet(viewsets.ModelViewSet):
    queryset = UserAPISecret.objects.all()
    serializer_class = UserAPISecretSerializer
    ordering = ("index",)
