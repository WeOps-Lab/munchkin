from django.http import JsonResponse

from apps.core.decorators.api_perminssion import HasRole


@HasRole(roles=["admin"])
def test(request):
    return JsonResponse({"result": True})
