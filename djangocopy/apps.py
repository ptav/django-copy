import os
import importlib
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.conf import settings

class DjangoCopyConfig(AppConfig):
    verbose_name = "Django-copy - probably the smallest CMS framework for Django"
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        super().ready()
        load_templates()


# list all html files in djangocopy/templates/djangocopy/templates 
# and in the project templates/djangocopt/templates folders and adds
# them to the djangocopy.models.Template model. Name is set to the 
# Templates table.
def load_templates():
    base_dir = os.path.dirname(importlib.util.find_spec('djangocopy').origin)
    root_dir = os.path.join(base_dir, 'templates', 'djangocopy', 'templates')
    __create_page_templates__(root_dir)
    
    user_dir = os.path.join(settings.BASE_DIR, 'templates', 'djangocopy', 'templates')
    # If exists
    # __create_page_templates__(user_dir)
    

def __create_page_templates__(dir):
    from .models import Template

    templates = [
        Template(label=flnm[:-5], template=flnm)
        for flnm in os.listdir(dir)
        if flnm.endswith('.html') and not Template.objects.filter(template__endswith=flnm)
    ]

    Template.objects.bulk_create(templates)

