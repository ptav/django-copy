from django.conf import settings
from django.template import Library
from django.utils.safestring import mark_safe
from ..models import Navbar


register = Library()


@register.simple_tag
def __djangocopy_load_libraries__():
    explicit = settings._explicit_settings

    stream = ""
    
    if 'DJANGOCOPY_ENABLE_BOOTSTRAP5' in explicit and settings.DJANGOCOPY_ENABLE_BOOTSTRAP5:
        stream += '<!--- Load Bootstrap v5 CSS -->'\
        '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">'\
        '<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">'\
        '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>'
    else:
        stream += '<!--- Load Bootstrap v4 CSS and jQuery -->'\
        '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">'\
        '<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>'\
        '<script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>'

    if 'DJANGOCOPY_ENABLE_HTMX' in explicit and settings.DJANGOCOPY_ENABLE_HTMX:
        stream += '<!--- Load HTMX -->'\
        '<script src="https://unpkg.com/htmx.org@1.8.6" integrity="sha384-Bj8qm/6B+71E6FQSySofJOUjA/gq330vEqjFx9LakWybUySyI1IQHwPtbTU7bNwx" crossorigin="anonymous"></script>'
    
    if 'DJANGOCOPY_ENABLE_ALPINEJS' in explicit and settings.DJANGOCOPY_ENABLE_ALPINEJS:
        stream += '<!--- Load alpine.js -->'\
        '<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>'
    
    if 'DJANGOCOPY_ENABLE_JQUERY' in explicit and settings.DJANGOCOPY_ENABLE_JQUERY:
        stream += '<!--- Load jQuery -->'\
        '<script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>'
    
    if 'DJANGOCOPY_ENABLE_FONTAWESOME' in explicit and settings.DJANGOCOPY_ENABLE_FONTAWESOME:
        stream += '<!-- Load Font Awesome and DjangoCopy CSS -->'\
        '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" integrity="sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+QkPxCAFlNEevoEH3Sl0sibVcOQVnN" crossorigin="anonymous">'

    stream += '<!-- Load DjangoCopy CSS -->'\
    '<link rel="stylesheet" href="/static/css/djangocopy.css">'

    return mark_safe(stream)


@register.inclusion_tag('djangocopy/navbar.html', takes_context=True)
def __djangocopy_navbar__(context):
    """
    Generate navbar

    DEVNOTE: Consider using Django-Sites to have difference navbar of each site
    """

    if hasattr(context, 'request') and hasattr(context.request, 'user'):
        user = context.request.user

        if user.is_anonymous:
            qs = Navbar.objects.filter(anonymous=True).order_by('-z_index').distinct()

        else:
            # First check if there are Navbar associated with this user's group, then look for a default one
            qs = Navbar.objects.filter(anonymous=False, groups__in=context.request.user.groups.all()).order_by('-z_index').distinct()
            if not qs.exists():
                qs = Navbar.objects.filter(anonymous=False, groups=None).order_by('-z_index').distinct()
            if not qs.exists():
                return {} # still nothing? return empty
    else:
        return {}

    logo = None
    elements = []
    for nav in qs:
        if nav.logo and not logo: logo = nav.logo.image.url
        elements += nav.elements

    #for e in navbar.elements:
    #    print(e)
    #    e['url'] = reverse(e['url'], args=e.get('args',None))

    return {
        'navbar_logo': logo, # if there are several navbars use only the first logo
        'navbar_items': elements,
    }


