import logging
from django.http import HttpResponseServerError
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.conf import settings

from .models import Page


logger = logging.getLogger(__name__)


def static_page(request,slug):
    try:
        page = Page.objects.filter(slug=slug).first()
        # slug has to be unique so qs will alsways be a single item
        
        # Check group permissions
        if page.groups.count():
            page = page.filter(groups__in=request.user.groups.all())
            if not page:
                raise PermissionDenied("Need additional permissions to view this page")
        
        # Check for authentication
        elif page.authenticated and not request.user.is_authenticated:
            raise PermissionDenied("Need to be signedin to view this page")
        
    except Exception as err:
        logger.error(f"Djangocopy error: {err}")
        return HttpResponseServerError(err)

    context = {
        'template': 'djangocopy/templates/' + page.template.template.name,
        'metadata': {
            'title':        page.title,
            'description':  page.description,
            'keywords':     page.keywords,
        }
    }
        
    return render(request, "djangocopy/wrapper.html", context)


def index(request):
    u = request.user
    if u.is_superuser or u.is_staff:
        return redirect('admin:index')
    else:
        return render(request, "djangocopy/default.html")


class BasicView():
    FORM_CLASS = None
    FORM_TEMPLATE = None
    FORM_TEMPLATE_VAR = 'form'

    def __call__(self, request, *args, **kwargs):
        if request.GET:
            return self.get(request, *args, **kwargs)
        
        elif request.POST:
            return self.post(request, *args, **kwargs)

        else:
            return self.unbound(request, *args, **kwargs)
            
    def get(self, request, *args, **kwargs):
        form = self.FORM_CLASS(request.GET)
        if form.is_valid():
            return self.get_is_valid(request, form, *args, **kwargs)
        else:
            return self.get_not_valid(request, form, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.FORM_CLASS(request.POST)
        if form.is_valid():
            return self.post_is_valid(request, form, *args, **kwargs)
        else:
            return self.post_not_valid(request, form, *args, **kwargs)

    def unbound(self, request, *args, **kwargs):
        context = {self.FORM_TEMPLATE_VAR: self.FORM_CLASS()}
        return render(request, self.FORM_TEMPLATE, context)

    def get_is_valid(self, request, form, *args, **kwargs):
        pass

    def get_not_valid(self, request, form, *args, **kwargs):
        context = {self.FORM_TEMPLATE_VAR: self.FORM_CLASS(form)}
        return render(request, self.FORM_TEMPLATE, context)

    def post_is_valid(self, request, form, *args, **kwargs):
        pass

    def post_not_valid(self, request, form, *args, **kwargs):
        context = {self.FORM_TEMPLATE_VAR: self.FORM_CLASS(form)}
        return render(request, self.FORM_TEMPLATE, context)
