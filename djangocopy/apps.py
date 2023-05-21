import os
import importlib
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.conf import settings

class DjangoCopyConfig(AppConfig):
    name = 'djangocopy'

    def ready(self):
        super().ready()
        post_migrate.connect(load_templates, sender=self)


# list all html files in djangocopy/templates/djangocopy/templates 
# and in the project templates/djangocopt/templates folders and adds
# them to the djangocopy.models.Template model. Name is set to the 
# Templates table.
def load_templates(sender, **kwargs):
    from .models import Template
    templates = []
    names = []

    base_dir = os.path.dirname(importlib.util.find_spec('djangocopy').origin)
    root_dir = os.path.join(base_dir, 'templates', 'djangocopy', 'templates')
    user_dir = os.path.join(settings.BASE_DIR, 'templates', 'djangocopy', 'templates')
    for f in os.listdir(root_dir) + os.listdir(user_dir):
        if f.endswith('.html'):
            if not Template.objects.filter(template__endswith=f):
               templates.append(Template(label=f[:-5], template=f))
    
    Template.objects.bulk_create(templates)

