from user_agents import parse
from django.conf import settings
from django.utils.translation import to_locale, get_language
from .models import Copy, PageVisit
from .utils import get_ip_address, get_client_country_code


class CopyMiddleware:
    "Load copy for the current page"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        # Load applicable copy into the request before running the function
        url = request.path
        locale = to_locale(get_language())
        geo = get_client_country_code(request)
        draft = request.user.is_authenticated and 'draft' in request.GET

        request.copy = Copy.get_for_url(url, locale, geo, draft)

        return self.get_response(request, *args, **kwargs)


def copy_decorator(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        middleware = CopyMiddleware(view_func)
        return middleware(request, *args, **kwargs)
    return _wrapped_view_func


class TrackMiddleware:
    "Log of page visits."

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        response = self.get_response(request, *args, **kwargs)
        # tracking is logged after the view is run

        # If request is unsuccesful, ignore it (default unless DJANGOCOPY_LOG_ALL_VISITS is True)
        if (not hasattr(settings, 'DJANGOCOPY_LOG_ALL_VISITS') or  \
            settings.DJANGOCOPY_LOG_ALL_VISITS == False) and \
            response.status_code != 200:
            return response

        # Code to be executed for each request/response after the view is called.
        try:
            url = request.build_absolute_uri()
            ip = get_ip_address(request)
            status_code = response.status_code
            user = request.user if request.user.is_authenticated else None
            referrer = request.META.get('HTTP_REFERER', '')
            user_agent_string = request.META.get('HTTP_USER_AGENT', '')
            session = request.session.session_key
            device_info = self.get_device_info(user_agent_string)
            language = get_language()

            PageVisit.objects.create(
                url=url,
                ip=ip,
                user=user,
                status_code=status_code,
                referrer=referrer,
                user_agent=user_agent_string,
                session=session,
                device_info=device_info,
                language=language,
            )

        except Exception as err:
            # You might want to log the error here or send it to an error tracking service
            pass

        return response

    @staticmethod
    def get_device_info(user_agent_string):
        try:
            ua = parse(user_agent_string)
            return ua.device.family
        except Exception as e:
            # Return 'Unknown' or any default value in case of an error
            return 'Unknown'


def track_decorator(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        middleware = TrackMiddleware(view_func)
        return middleware(request, *args, **kwargs)
    return _wrapped_view_func
