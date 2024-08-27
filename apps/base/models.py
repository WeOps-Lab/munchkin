import binascii
import os

from django.db import models

from apps.core.models.time_info import TimeInfo


class UserAPISecret(TimeInfo):
    username = models.CharField(max_length=255, unique=True)
    api_secret = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        if not self.api_secret:
            self.api_secret = self.generate_api_secret()
        return super(UserAPISecret, self).save(*args, **kwargs)

    @staticmethod
    def generate_api_secret():
        return binascii.hexlify(os.urandom(32)).decode()
