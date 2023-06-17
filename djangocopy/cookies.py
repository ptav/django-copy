import logging
from datetime import datetime
from django import forms
from django.shortcuts import render, redirect
from django.conf import settings

from .views import BasicView


logger = logging.getLogger(__name__)


class CookieConsentForm(forms.Form):
    """Cookies consent form"""
    necessary = forms.BooleanField(initial=True, disabled=True, help_text='Necessary cookies are enabled always')
    preferences = forms.BooleanField(required=False, help_text='Cookies used to store your preferences and settings')
    functional = forms.BooleanField(required=False, help_text='3rd party cookies used to deliver additional functionality')
    marketing = forms.BooleanField(required=False, help_text='Cookies used to deliver and target advertising')


def cookie_consent(request):
    """Retrieve cookie configuration
    
    Return:
        List of cookie consent categories. None if cookies are not configured
    """

    cookie_consent = request.session.get('cookie_consent')

    if not cookie_consent:
        return False
    
    config = [k for k,v in cookie_consent.items() if v and k != '__timestamp__']    
    return config


def has_cookie_consent(request, cookie_type=None):
    """Check cookie configuration
    
    Args:
        cookie_type: If None, check if cookies have been configured, otherwise
        Check specific cookie category ('necessary', 'preferences', 'functional' 
        or 'marketing')
    """

    cookie_consent = request.session.get('cookie_consent')
    if not cookie_consent:
        return False
    
    if cookie_type is None: # only checking cookies have been configured
        return True
    
    return cookie_consent.get(cookie_type, False)



class CookieConsent(BasicView):
    """Cookies consent form view"""
    
    FORM_TEMPLATE = 'djangocopy/cookie_consent.html'
    FORM_CLASS = CookieConsentForm
    FORM_VAR = 'cookie_consent_form'

    def unbound(self, request):
        request.session['next'] = request.META.get('HTTP_REFERER', '/')
        
        if has_cookie_consent(request):
            form = self.FORM_CLASS(initial=request.session['cookie_consent'])
        else:
            form = self.FORM_CLASS()
                
        return render(request, self.FORM_TEMPLATE, {self.FORM_VAR: form})

    def post_is_valid(self, request, form):
        request.session['cookie_consent'] = {
            'necessary': form.cleaned_data['necessary'],
            'preferences': form.cleaned_data['preferences'],
            'functional': form.cleaned_data['functional'],
            'marketing': form.cleaned_data['marketing'],
            '__timestamp__': datetime.now().isoformat(),
        }
        return redirect(request.session.get('next', '/'))
