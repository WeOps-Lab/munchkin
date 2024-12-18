import json

from django.http import JsonResponse

from apps.core.logger import logger
from apps.core.utils.exempt import api_exempt


@api_exempt
def test(request):
    params = json.loads(request.body)
    logger.info(f"receive wechat msg {request.body}")
    return JsonResponse(params)
