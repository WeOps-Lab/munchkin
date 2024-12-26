from django.http import HttpResponse
from wechatpy import parse_message
from wechatpy.replies import TextReply

from apps.base.utils import WeChatUtils
from apps.core.logger import logger
from apps.core.utils.exempt import api_exempt


@api_exempt
def test(request):
    logger.info(f"wechat params : {request.GET.dict()}, body: {request.body}")
    signature_check_result = WeChatUtils.signature_check(request.GET)
    if request.method == "GET":
        if signature_check_result:
            return HttpResponse(request.GET.get("echostr"))
        else:
            return HttpResponse("Access failed!")

    if request.method == "POST":
        if not signature_check_result:
            return HttpResponse("Access failed!")

        msg = parse_message(request.body)
        reply = TextReply(message=msg)
        if msg.type == "text":
            reply.content = "已收到您的消息，感谢支持统一告警中心！"
        elif msg.type == "event":
            if msg.event in ["subscribe_scan", "scan"]:
                reply.content = "感谢关注统一告警中心！"
            elif msg.event == "unsubscribe":
                reply.content = ""
        else:
            reply.content = "感谢关注统一告警中心！"

        xml = reply.render()
        return HttpResponse(xml)
