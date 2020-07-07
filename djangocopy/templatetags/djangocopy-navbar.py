from django.template import Library
from djangocopy.models import Page, Copy, Navbar


register = Library()


@register.inclusion_tag('djangocopy/navbar.html', takes_context=True)
def navbar(context):
    """
    Generate navbar

    DEVNOTE: Consider using Django-Sites to have difference navbar of each site
    """

    if hasattr(context, 'request') and hasattr(context.request, 'user'):
        # First check if there are Navbar associated with this user's group, then look for a default one
        qs = Navbar.objects.filter(groups__in=context.request.user.groups.all()).order_by('-z_index').distinct()
        if not qs.exists():
            qs = Navbar.objects.filter(groups=None) # return default navbar
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