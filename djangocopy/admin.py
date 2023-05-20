from django import forms
from django.shortcuts import redirect
from django.contrib import admin

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Template, Image, Page, Copy, Navbar, PageVisit



ELEMENTS_HELPTEXT = \
"""
Simple entry: { 'label':"Home", url:"/" }
Add image: { 'label':"Logout", url:"/accounts/logout", img:"/avatar.jpg" }
Add FA icon: { 'label':"Login", url:"/accounts/login", faicon:"fa-signin" }
Dropdown (and example of divider):  
    {
        "label":" ",
        "img":"/game/useravatar",
        "dropdown":[
            { "label":"Profile", "url":"/game/profile", "divider":1 },
            { "label":"Sign-out", "url":"/accounts/logout" }
        ]
    }

"""

@admin.register(Navbar)
class NavbarAdmin(admin.ModelAdmin):
    model = Navbar

    list_display = ('label', 'get_groups', 'anonymous', 'z_index', )
    autocomplete_fields = ('groups', )

    help_texts = {
        'elements': ELEMENTS_HELPTEXT,
    }

    def get_groups(self, obj):
        txt = ""
        for grp in obj.groups.all():
            txt += ', ' + grp.name
        return txt[2:] if len(txt) > 2 else ""
    get_groups.short_description = 'Groups'


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    model = Page

    ordering= ('slug', )
    list_display = ('slug', 'template', )
    search_fields = ('slug', )

    fieldsets = (
        (None, {
            'fields': ('slug', 'template', 'authenticated', 'groups')
        }),
        ('SEO', {
            #'classes': ('collapse', ),
            'fields': ('title', 'description', 'keywords', ),
        }),
    )



def publish_drafts(modeladmin, request, queryset):
    for obj in queryset:
        pub, created = Copy.objects.get_or_create(
            url=obj.url,
            fieldid=obj.fieldid,
            locale=obj.locale,
            geo=obj.geo,
            status=Copy.STATUS_PUBLISHED,
        )

        pub.text = obj.text
        pub.format = obj.format
        pub.save()

        obj.delete()

    return redirect(request.path)



class CopyAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CopyAdminForm, self).__init__(*args, **kwargs)

        if self.instance is None or self.instance.format == Copy.FORMAT_SAFE_HTML:
            self.fields['text'].widget = CKEditorUploadingWidget()

    class Meta:
        model = Copy
        fields = '__all__'



@admin.register(Copy)
class CopyAdmin(admin.ModelAdmin):
    model = Copy
    form = CopyAdminForm
    actions = (publish_drafts, )

    ordering= ('url', 'fieldid', 'locale', 'geo', '-status')
    list_display = ('fieldid', 'url', 'locale', 'geo', 'short_text', 'format', 'status')
    list_filter = ('status', 'locale', 'geo', 'url', 'fieldid')
    search_fields = ('text', 'locale', 'geo', 'fieldid', 'url')


@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.get_fields()]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Template)
admin.site.register(Image)
