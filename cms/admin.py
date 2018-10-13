from django import forms
from django.shortcuts import redirect
from django.contrib import admin

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Template, Page, Copy, Navbar



@admin.register(Navbar)
class NavbarAdmin(admin.ModelAdmin):
    model = Navbar

    list_display = ('id', 'get_groups', )
    autocomplete_fields = ('groups', )

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
    list_display = ('id', 'slug', 'template', )
    search_fields = ('slug', )

    fieldsets = (
        (None, {
            'fields': ('slug', 'template', )
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
    list_display = ('url', 'fieldid', 'locale', 'geo', 'short_text', 'format', 'status')
    list_editable = ('status', )
    list_filter = ('status', 'locale', 'geo', 'url', 'fieldid')
    search_fields = ('text', 'locale', 'geo', 'fieldid', 'url')


admin.site.register(Template)
