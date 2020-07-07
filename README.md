# django-copy

Probably the smallest and simplest djangocopy for Django.

While it is extremely simple, it supports some features that I haven't found in other djangocopy frameworks out there. Namely you can create pages for **multiple languages** but also for **multiple locations** or any conbination of both


## Installation

1. Use pip to instal the latest stable release

    ```
    pip install django-copy
    ```

    You can also install a local copy by running `setup.py install` at the top directory of django-copy


2. Add `djangocopy` to `INSTALLED_APPS` in the project settings (see dependencies below)

3. Setup `DJANGOCOPY_TEMPLATE_ROOT` and `DJANGOCOPY_IMAGE_ROOT` to define where uploaded template and image files are stored. For example:

    ```
    DJANGOCOPY_TEMPLATE_ROOT = 'templates'
    DJANGOCOPY_IMAGE_ROOT = 'images'
    ```

    the above settings will upload templates to `MEDIA_ROOT/templates`

4. Add the  media folder to the `DIRS` list in `TEMPLATES` in order to serve uploaded templates. For example (if `DJANGOCOPY_TEMPLATE_ROOT` is set as above and `BASE_DIR` points to the project root folder):

    ```
    TEMPLATES = [
        {
            ...
            'DIRS': ['media/'],
            ...
        },
    ]
    ```

5. Add `djangocopy.middleware.LocalisationMiddleware` to `MIDDLEWARE` in the project settings file (OR see alternative below)

6. If not set already, set `MEDIA_ROOT` and `MEDIA_URL` in settings


### Dependencies:

In _settings.py_ add:

```
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sitemaps',

    ...

    'ckeditor',
    'ckeditor_uploader',

    'simple_history',

    'djangocopy',

    ...
]

...

# django.contrib.auth settings
#

LOGIN_URL = '/accounts/login'

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/accounts/login'


# CKEditor
#

CKEDITOR_BASEPATH = "{}ckeditor/ckeditor/".format(STATIC_URL)

CKEDITOR_UPLOAD_PATH = 'uploads/'

CKEDITOR_CONFIGS = {
    ...
}
```

In _urls.py_ add

```
path('ckeditor/', include('ckeditor_uploader.urls')),
path('accounts/', include('django.contrib.auth.urls')),
path('filer/', include('filer.urls')),
path('djangocopy/', include('djangocopy.urls')),
```




### Optional:

#### Localisation Middleware
If you follow step 6 above, all views in the project will get access to the content stored in the djangocopy app. That carries a small overhead so if you want to avoid that you can instead add `@decorator_from_middleware(LocalisationMiddleware)` to each of the views that will require access to DB stored content.

For example:

```
from django.utils.decorators import decorator_from_middleware
from djangocopy.middleware import LocalisationMiddleware

@decorator_from_middleware(LocalisationMiddleware)
def my_view
    ...
```


## Open source licenses

This product depends on the following software and media packages

GeoLite2 data created by MaxMind, available from [http://www.maxmind.com](http://www.maxmind.com)

Font Awesome fonts version 4.7 is licensed under [SIL OFL 1.1](http://scripts.sil.org/OFL) and the [MIT License](http://opensource.org/licenses/mit-license.html)

Bootstrap version 4.0 is licensed under the [MIT License](http://opensource.org/licenses/mit-license.html)
