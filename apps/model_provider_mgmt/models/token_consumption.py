from django.db import models


class TokenConsumption(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    input_tokens = models.BigIntegerField()
    output_tokens = models.BigIntegerField()
    username = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
