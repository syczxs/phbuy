
import time

from django.http import HttpResponse
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.utils.deprecation import MiddlewareMixin

import redis

conn = redis.Redis(host='127.0.0.1', port=6379)

class md(MiddlewareMixin):
    def process_request(self,request):
        ip_client=request.META.get('REMOTE_ADDR')
        now =float(time.time())
        print(now,'aaaaaaaa')
        a=float(conn.getset(ip_client,now ).decode(encoding='utf-8'))
        delta = now-a
        print(delta)
        if delta<1:
            return HttpResponse('操作太过频繁')


MOBILE_USERAGENTS = ("2.0 MMP", "240x320", "400X240", "AvantGo", "BlackBerry",
                     "Blazer", "Cellphone", "Danger", "DoCoMo", "Elaine/3.0", "EudoraWeb",
                     "Googlebot-Mobile", "hiptop", "IEMobile", "KYOCERA/WX310K", "LG/U990",
                     "MIDP-2.", "MMEF20", "MOT-V", "NetFront", "Newt", "Nintendo Wii", "Nitro",
                     "Nokia", "Opera Mini", "Palm", "PlayStation Portable", "portalmmm", "Proxinet",
                     "ProxiNet", "SHARP-TQ-GX10", "SHG-i900", "Small", "SonyEricsson", "Symbian OS",
                     "SymbianOS", "TS21i-10", "UP.Browser", "UP.Link", "webOS", "Windows CE",
                     "WinWAP", "YahooSeeker/M1A1-R2D2", "iPhone", "iPod", "Android",
                     "BlackBerry9530", "LG-TU915 Obigo", "LGE VX", "webOS", "Nokia5800")




