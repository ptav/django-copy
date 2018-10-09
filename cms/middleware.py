import os

from django.http import Http404
from django.utils.translation import to_locale, get_language
from django.contrib.gis.geoip2 import GeoIP2

from .models import Copy


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
GEOIP_PATH = os.path.join(BASE_PATH,'geoip2')


def get_ip_address(request):
    "Map request to external IP address resolving internal address if necessary"

    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')

    if forwarded:
        ip = forwarded.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip



def ip_to_country_code(addr, default_code='GB'):
    "Map request to client's country based on IP address"

    if addr == '127.0.0.1' or addr == 'localhost':
        return default_code

    g = GeoIP2(path=GEOIP_PATH)
    return g.country(addr)['country_code']



def get_client_country_code(request):
    "Shorthand to request country code directly from request"
    return ip_to_country_code(get_ip_address(request))



class LocalisationMiddleware(object):

    def process_request(self, request):
        url = request.path
        locale = to_locale(get_language())
        geo = get_client_country_code(request)
        draft = request.user.is_authenticated and 'draft' in request.GET

        request.copy = Copy.get_for_url(url, locale, geo, draft)

        return
