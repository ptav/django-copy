import os
from django.http import Http404
from django.utils.translation import to_locale, get_language
from django.contrib.gis.geoip2 import GeoIP2
from django.conf import settings
from .models import Copy


GEOIP_PATH = settings.GEOIP_PATH


def get_ip_address(request):
    "Map request to external IP address resolving internal address if necessary"

    standardised_headers = {key.lower(): value for key, value in request.headers.items()}

    if "x-forwarded-for" in standardised_headers:
        return standardised_headers.get("x-forwarded-for").split(',')[0]
    elif "forwarded" in standardised_headers:
        # Header format: "Forwarded": "for=<for_ip>, for=<proxy_ip>;host=<host>;proto=https"
        # Extract the for=... component
        forwarded_for = next(
            component.lower() for component in request.headers.get("Forwarded").split(";")
            if component.lower().startswith("for")
        )
        # Get the first IP address in the redirect chain (original client)
        ip_address = forwarded_for.strip("for=").split(",")[0]

        return ip_address
    else:
        return request.META.get('REMOTE_ADDR')


def ip_to_country_code(addr, default_code='GB'):
    "Map request to client's country based on IP address"

    if addr == '127.0.0.1' or addr == 'localhost':
        return default_code

    g = GeoIP2(path=GEOIP_PATH)
    return g.country(addr)['country_code']


def get_client_country_code(request):
    "Shorthand to request country code directly from request"
    return ip_to_country_code(get_ip_address(request))


class LocalisationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url = request.path
        locale = to_locale(get_language())
        geo = get_client_country_code(request)
        draft = request.user.is_authenticated and 'draft' in request.GET

        request.copy = Copy.get_for_url(url, locale, geo, draft)

        return self.get_response(request)
