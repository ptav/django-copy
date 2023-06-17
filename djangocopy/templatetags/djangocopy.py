from uuid import uuid4
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import to_locale, get_language
from django.template import Library, Node, TemplateSyntaxError

from ..models import Copy
from ..cookies import cookie_consent, has_cookie_consent


register = Library()


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
def glyphicon(name,aria_text=None,options=None,aria_hidden=False):
    "HTML for inserting a Bootstrap 3 glyph icon. 'aria_hidden' should be True if icon is purely decorative."
    return mark_safe('<span class="glyphicon glyphicon-{} {}" aria-hidden="{}" aria-text="{}"></span>'.format(name,options,str(aria_hidden).lower(),aria_text))


@register.simple_tag
def faicon(name, aria_text='', options='', aria_hidden=True):
    "HTML for inserting a Font Awesome icon. 'aria_hidden' should be True if icon is purely decorative. 'options' can be fa-lg, fa-order, fa-pull-right and others"
    return mark_safe('<i class="fa fa-{} {}" aria-hidden="{}" aria-text="{}"></i>'.format(name,options,str(aria_hidden).lower(),aria_text))


@register.simple_tag(name='cookie_consent', takes_context=True)
def cookie_consent_tag(context):
    """
    Retrieve cookies consent status
    
    Return:
        list of consent categories
    """
    request = context['request']
    return cookie_consent(request)


@register.simple_tag(name='has_cookie_consent', takes_context=True)
def has_cookie_consent_tag(context, cookie_type=None):
    """
    Check cookies consent status
    
    Args:
        cookie_type: If None, check if cookies have been configured, otherwise
        Check specific cookie category ('necessary', 'preferences', 'functional' 
        or 'marketing')
    """
    request = context['request']
    return has_cookie_consent(request)


@register.inclusion_tag('djangocopy/widgets/modal.html', takes_context=True)
def insert_modal(
    context,
    id,
    title = 'Replace this placeholder with a "title" argument',
    body_template = False,
    body_content = 'Replace this placeholder with a "body" or "body_template" argument',
    footer_template = False,
    footer_content = '',
    dismissable = True,
    fade = True,
    show = False):
    
    return {
        'id': id,
        'title': title,
        'body_template': body_template,
        'body_content': body_content,
        'footer_template': footer_template,
        'footer_content': footer_content,
        'dismissable': dismissable,
        'fade': fade,
        'show': show,
        'request': context.request,
    }


@register.filter
def list_to_2_column(objects):
    "Convert a list into 2 sub-lists of similar size. Usually used to break a long list of objects into columns"
    sz = int(len(objects) / 2. + 0.51)
    if sz:
        return [objects[:sz],objects[sz:]]
    else:
        return [objects]


@register.filter
def list_to_3_column(objects):
    "Convert a list into 3 sub-lists of similar size. Usually used to break a long list of objects into columns"
    sz = int(len(objects) / 3. + 0.63)
    if sz:
        return [objects[:sz],objects[sz:2*sz],objects[2*sz:]]
    else:
        return [objects]


@register.filter
def list_to_4_column(objects):
    "Convert a list into 4 sub-lists of similar size. Usually used to break a long list of objects into columns"
    sz = int(len(objects) / 4. + 0.76)
    if sz:
        return [objects[:sz],objects[sz:2*sz],objects[2*sz:3*sz],objects[3*sz:]]
    else:
        return [objects]


# Based on UUID Template Tag, https://djangosnippets.org/snippets/1356/
#

class UUIDNode(Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render( self, context ):
        context[self.var_name] = str(uuid4())
        return ''

@register.tag(name='uuid')
def uuid_tag(parser,token):
    """
    Generate a random UUID and store it in a named context variable.

    Sample usage:
        {% uuid varname %}
        varname will contain the generated UUID
    """
    try:
        tagname, varname = token.contents.split()
    except ValueError:
        raise TemplateSyntaxError("{} tag requires exactly one argument".format(token.contents.split()[0]))

    return UUIDNode(varname)
