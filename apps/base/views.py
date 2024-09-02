from rest_framework import status, viewsets
from rest_framework.response import Response

from apps.base.models import UserAPISecret
from apps.base.user_api_secret_mgmt.serializers import UserAPISecretSerializer


class UserAPISecretViewSet(viewsets.ModelViewSet):
    queryset = UserAPISecret.objects.all()
    serializer_class = UserAPISecretSerializer
    ordering = ("-id",)

    def list(self, request, *args, **kwargs):
        queryset = UserAPISecret.objects.filter(username=request.userinfo.get("username"))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        kwargs = {"username": request.userinfo.get("username"), "api_secret": UserAPISecret.generate_api_secret()}
        serializer = self.get_serializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
