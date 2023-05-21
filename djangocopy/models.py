from markdown import markdown
from json import loads
import os, importlib

from django.db import models
from django.db.models import Q
from django.urls import resolve
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.sessions.models import Session
from simple_history.models import HistoricalRecords


class Template(models.Model):
    "HTML Templates"
    template = models.FileField(upload_to=settings.DJANGOCOPY_TEMPLATES)
    label = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.label if self.label else self.template.name


class Image(models.Model):
    "Image Files"

    image = models.ImageField(upload_to=settings.DJANGOCOPY_IMAGES)
    label = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.label if self.label else self.image.name


class Page(models.Model):
    "Definition for pages managed by the djangocopy"

    slug = models.SlugField(max_length=255, unique=True)
    template = models.ForeignKey(Template, on_delete=models.PROTECT)
    authenticated = models.BooleanField(default=False, help_text="If True, visitor must login to access this page")
    groups = models.ManyToManyField(Group, blank=True, help_text="If populated, only members of these groups can view the page (authenticated flag is then ignored).")

    title = models.CharField(max_length=255,default='', blank=True)
    description = models.CharField(max_length=255,default='', blank=True)
    keywords = models.CharField(max_length=255,default='', blank=True)

    history = HistoricalRecords()

    @property
    def get_title(self):
        return self.title if self.title else self.slug


class Navbar(models.Model):
    "Navbar links"

    label = models.CharField(max_length=255)
    logo = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True, help_text="A picture to use as a logo")
    groups = models.ManyToManyField(Group, blank=True, help_text="Associate navbar with a particular user group.")
    elements = models.JSONField()
    z_index = models.IntegerField(default=0, help_text="The z-index determines the order of navbar items. A higher value appears first.")
    anonymous = models.BooleanField(default=False, help_text="If True, navbar is shown to anonymous users. If False (default), navbar is shown to authenticated users only.")

    history = HistoricalRecords()


class Copy(models.Model):
    "djangocopy content"

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

    fieldid = models.SlugField(max_length=100,help_text="The field identifier that will be used in templates")

    url = models.CharField(max_length=255,blank=True,help_text="URL name (leave empty to load for all templates)")
    locale = models.CharField(max_length=5,blank=True,help_text="Browser settings (e.g. 'en_GB')")
    geo = models.CharField(max_length=2,blank=True,help_text="Country code derived from the IP (e.g. 'GB')")

    text = models.TextField(max_length=10000)
    format = models.CharField(max_length=1,choices=FORMAT_CHOICES,default=FORMAT_PLAIN)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=STATUS_DRAFT)

    history = HistoricalRecords()


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



__MAPPING__ = {
    Copy.FORMAT_PLAIN: lambda txt: txt,
    Copy.FORMAT_MARKDOWN: lambda txt: mark_safe(markdown(txt)),
    Copy.FORMAT_JSON: lambda txt: __map_json__(txt),
    Copy.FORMAT_SAFE_HTML: lambda txt: mark_safe(txt),
    Copy.FORMAT_SPECIAL_HTML: lambda txt: mark_safe(txt),
}

def __map_json__(txt):
    try:
        return loads(txt)

    except Exception as e:
        # log error and fail silently
        logging.error('Error decoding JSON copy: {} ({})'.format(txt,e))


class PageVisit(models.Model):
    "Log of page visits. Works together with PageVisitMiddleware in middleware.py"

    time = models.DateTimeField(auto_now_add=True)
    url = models.URLField()
    status_code = models.IntegerField()
    ip = models.GenericIPAddressField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    referrer = models.URLField()
    user_agent = models.TextField()
    session = models.CharField(max_length=40, null=True)
    device_info = models.TextField()
    language = models.CharField(max_length=5)

    def __str__(self):
        return f'{self.time} {self.user} {self.status_code} {self.url}'
