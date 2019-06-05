from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import to_locale, get_language

from djangocopy.models import Page, Copy, Navbar

register = template.Library()



@register.filter()
def numeric_range(size):
    "Convert integer to a range (for numeric for loops generally)"
    return range(size)



@register.simple_tag
def getcopy(id):
    lang = to_locale(get_language())
    lang = 'en_GB' if lang == 'en_GB' or lang == 'en' else 'en'
    copy = Copy.objects.values_list('fieldid','text_'+lang)
    return dict(copy)



@register.simple_tag
def faicon(name, aria_text='', options='', aria_hidden=True):
    "HTML for inserting a Font Awesome icon. 'aria_hidden' should be True if icon is purely decorative. 'options' can be fa-lg, fa-order, fa-pull-right and others"
    return mark_safe('<i class="fa fa-{} {}" aria-hidden="{}" aria-text="{}"></i>'.format(name,options,str(aria_hidden).lower(),aria_text))



@register.inclusion_tag('djangocopy/widgets/navbar.html', takes_context=True)
def navbar(context):
    """
    Generate navbar
    :param game: Game PK
    :param player: Player PK
    :param number: Number of levels
    :returns: dictionary of data for the navbar tamplate

    NOTES: Consider using Django-Sites to have difference navbar of each site
    """

    # First check if there are Navbar associated with this user's group, then look for a default one
    qs = Navbar.objects.filter(groups__in=context.request.user.groups.all()).order_by('-z_index')
    if not qs.exists(): qs = Navbar.objects.filter(groups=None)
    if not qs.exists(): return {} # nothing found, return empty

    logo = None
    elements = []
    for navbar in qs:
        if not logo: logo = navbar.logo
        elements += navbar.elements

    #for e in navbar.elements:
    #    print(e)
    #    e['url'] = reverse(e['url'], args=e.get('args',None))

    return {
        'navbar_logo': logo, # if there are several navbars use only the first logo
        'navbar_items': elements,
    }
