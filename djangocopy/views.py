from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.decorators import decorator_from_middleware

from .middleware import LocalisationMiddleware
from .models import Page


@decorator_from_middleware(LocalisationMiddleware)
def static_page(request,slug):
    try:
        page = Page.objects.get(slug=slug)
        if page.authenticated and not request.user.is_authenticated: raise Http404
        
        template = page.template.template.name
        metadata = {
            'title':        page.title,
            'description':  page.description,
            'keywords':     page.keywords,
        }

    except:
        raise Http404

    return render(request, "djangocopy/wrapper.html", context={'template': template, 'metadata': metadata})



def index(request):
    u = request.user
    if u.is_superuser or u.is_staff:
        return redirect('admin:index')
    else:
        return render(request, "djangocopy/default.html")



class BasicView():
    FORM_CLASS = None

    def get(self, request, *args, **kwargs):
        form = self.FORM_CLASS(request.GET)
        if form.is_valid():
            return self.form_is_valid(form)
        else:
            return self.form_is_not_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.FORM_CLASS(request.POST)
        if form.is_valid():
            return self.form_is_valid(form)
        else:
            return self.form_is_not_valid(form)

    def unbound(self, request, *args, **kwargs):
        pass

    def form_is_valid(self, form):
        pass

    def form_is_not_valid(self, form):
        pass

    def __call__(self, request, *args, **kwargs):
        if request.GET:
            return self.get(request, *args, **kwargs)
        
        elif request.POST:
            return self.post(request, *args, **kwargs)

        else:
            return self.unbound(request, *args, **kwargs)