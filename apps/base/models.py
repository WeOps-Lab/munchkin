import binascii
import os

from django.db import models

from apps.core.models.time_info import TimeInfo


class UserAPISecret(TimeInfo):
    username = models.CharField(max_length=255, unique=True)
    api_secret = models.CharField(max_length=64)

    @staticmethod
    def generate_api_secret():
        return binascii.hexlify(os.urandom(32)).decode()
