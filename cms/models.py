from markdown import markdown
from json import loads
from jsonfield import JSONField

from django.db import models
from django.db.models import Q
from django.urls import resolve
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import Group



@python_2_unicode_compatible
class Template(models.Model):
    "HTML Templates"

    label = models.CharField(max_length=255)
    template = models.FileField(upload_to=settings.CMS_TEMPLATE_ROOT)

    def __str__(self):
        return self.label



@python_2_unicode_compatible
class Page(models.Model):
    "Definition for pages managed by the CMS"

    slug = models.SlugField(max_length=255, unique=True)
    template = models.ForeignKey(Template, on_delete=models.PROTECT)
    authenticated = models.BooleanField(default=False, help_text="If True, visitor must login to access this page")

    title = models.CharField(max_length=255,default='', blank=True)
    description = models.CharField(max_length=255,default='', blank=True)
    keywords = models.CharField(max_length=255,default='', blank=True)

    @property
    def get_title(self):
        return self.title if self.title else self.slug



@python_2_unicode_compatible
class Navbar(models.Model):
    "Navbar links"

    logo = models.ImageField(null=True, blank=True, upload_to='cms/',help_text="A picture to use as a logo")
    groups = models.ManyToManyField(Group, blank=True, help_text="Associate navbar with a particular user group.")
    elements = JSONField()
    z_index = models.IntegerField(default=0, help_text="The z-index determines the order of navbar items. A higher value appears first.")



@python_2_unicode_compatible
class Copy(models.Model):
    "CMS content"

    FORMAT_PLAIN = 'p'
    FORMAT_MARKDOWN = 'm'
    FORMAT_JSON = 'j'
    FORMAT_SAFE_HTML = 'h'
    FORMAT_SPECIAL_HTML = 's'

    FORMAT_CHOICES = (
        (FORMAT_PLAIN,'Plain text'),
        (FORMAT_MARKDOWN,'Markdown'),
        (FORMAT_JSON,'JSON'),
        (FORMAT_SAFE_HTML,'HTML'),
        (FORMAT_SPECIAL_HTML,'Special HTML'),
    )

    STATUS_DRAFT = 'd'
    STATUS_PUBLISHED = 'p'

    STATUS_CHOICES = (
        (STATUS_DRAFT,'Draft'),
        (STATUS_PUBLISHED,'Published'),
    )

    url = models.CharField(max_length=255,blank=True,help_text="URL name (leave empty to load for all templates)")
    fieldid = models.SlugField(max_length=100,help_text="The field identifier that will be used in templates")

    locale = models.CharField(max_length=5,blank=True,help_text="Browser settings (e.g. 'en_GB')")
    geo = models.CharField(max_length=2,blank=True,help_text="Country code derived from the IP (e.g. 'GB')")

    text = models.TextField(max_length=10000)
    format = models.CharField(max_length=1,choices=FORMAT_CHOICES,default=FORMAT_PLAIN)

    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=STATUS_DRAFT)

    class Meta:
        verbose_name_plural = 'copy'
        unique_together = (("fieldid","url","locale","geo","status"),)

    @property
    def status_as_string(self):
        return dict(self.STATUS_CHOICES).get(self.status, '--')

    def render(self):
        return __MAPPING__[self.format](self.text)

    def short_text(self,truncate=80):
        return self.text[:truncate] + '...' if len(self.text) > truncate else self.text

    def __str__(self):
        str = "{}/{} - {}".format(self.url or '*',self.fieldid,self.text[:40])
        if self.locale or self.geo: str += " ({},{})".format(self.locale or '*',self.geo or '*')
        str += ' ' + self.status_as_string.upper()
        return str

    @staticmethod
    def get_for_url(url, locale, geo, draft=False):
        """Retrieve set of copies for a given URL (or URL name), locale and geographical location"""
        if draft:
            qs = Copy.objects.filter(
                Q(url=url) | Q(url=resolve(url).url_name) | Q(url=''),
                Q(locale=locale) | Q(locale=locale[:2]) | Q(locale=''),
                Q(geo=geo) | Q(geo=''),
            ).order_by('locale', 'geo', '-status') # Ordering puts defaults first so they get overwritten when converting to dict

        else:
            qs = Copy.objects.filter(
                Q(url=url) | Q(url=resolve(url).url_name) | Q(url=''),
                Q(locale=locale) | Q(locale=locale[:2]) | Q(locale=''),
                Q(geo='') | Q(geo=geo),
                status = Copy.STATUS_PUBLISHED,
            ).order_by('locale', 'geo') # Ordering puts defaults first so they get overwritten when converting to dict

        values = qs.values_list('fieldid', 'text', 'format')
        out = [(fld, __MAPPING__[fmt](txt)) for fld, txt, fmt in values]
        return dict(out)



def __map_json__(txt):
    try:
        return loads(txt)
    except Exception as e:
        logging.error('Error decoding JSON copy: {} ({})'.format(txt,e))
        pass # log error and fail silently


__MAPPING__ = {
    Copy.FORMAT_PLAIN: lambda txt: txt,
    Copy.FORMAT_MARKDOWN: lambda txt: mark_safe(markdown(txt)),
    Copy.FORMAT_JSON: lambda txt: __map_json__(txt),
    Copy.FORMAT_SAFE_HTML: lambda txt: mark_safe(txt),
    Copy.FORMAT_SPECIAL_HTML: lambda txt: mark_safe(txt),
}

