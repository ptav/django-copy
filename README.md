# django-copy

Probably the smallest and simplest djangocopy for Django.

While it is extremely simple, it supports some features that I haven't found in other CMS frameworks. Namely you can create 
pages for multiple languages but also for multiple locations or any conbination of both.


## Usage


## Installation

Use pip to instal the latest stable release.

```
pip install django-copy
```

Then add `djangocopy` and it's dependencies to `INSTALLED_APPS` in the project settings (see dependencies below)

    ```
    'ckeditor',
    'ckeditor_uploader',
    'easy_thumbnails',
    'filer',
    'mptt',
    'simple_history',
    'djangocopy',
    ```


## Configuration

1. If not set already, set `MEDIA_ROOT` and `MEDIA_URL` in settings. For example:

    ```
    MEDIA_ROOT = BASE_DIR.joinpath('media')
    MEDIA_URL = '/media/'
    ```

2. Also in settings, add `DJANGOCOPY_IMAGES` to define where uploaded template and imagefiles are stored. These paths will sit below `MEDIA_ROOT`. For example:

    ```
    DJANGOCOPY_IMAGES = 'copy/images/'
    ```

3. Middleware

    to automatically add required copy to a view, add `djangocopy.middleware.CopyMiddleware` to `MIDDLEWARE` in the project settings file

    To enable the cookie consent form add `djangocopy.middleware.CookieConsentMiddleware`

    To enable automated page visit tracking ad `djangocopy.middleware.TrackMiddleware`


4. In _urls.py_ add

    ```
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('filer/', include('filer.urls')),
    path('copy/', include('djangocopy.urls')),
    ```

5. Flag which 3rd party libraries you want to import into the site by setting each of the following flags to True. If not define these are assumed to be False:

    ```
    DJANGOCOPY_ENABLE_BOOTSTRAP4 = True
    DJANGOCOPY_ENABLE_BOOTSTRAP5 = False
    DJANGOCOPY_ENABLE_HTMX = True
    DJANGOCOPY_ENABLE_FONTAWESOME = True
    DJANGOCOPY_ENABLE_ALPINEJS = True
    ```

6. If using Bootstrap, align the django ERROR message with the Bootstrap DANGER message

```
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}
```

7. Setting `DJANGOCOPY_SITE_TITLE` is also advisable. It will be used as alt text for the logo if that is set, or to fill the home button in the navbar.

    ```
    DJANGOCOPY_SITE_TITLE = 'MySite'
    ```



### Dependencies:

Django-copy depends on the following packages that need to be installed separately

    ```
    markdown
    django-simple-history
    django-ckeditor
    django-ckeditor-filer
    ```

to configure these please add the following sample configuration in settings:

    ```
    # django.contrib.auth settings
    #

    LOGIN_URL = '/accounts/login'
    LOGIN_REDIRECT_URL = '/djangocopy/sample'
    LOGOUT_REDIRECT_URL = '/accounts/login'


    # CKEditor
    #

    CKEDITOR_BASEPATH = "{}ckeditor/ckeditor/".format(STATIC_URL)
    CKEDITOR_UPLOAD_PATH = 'uploads/'

    CKEDITOR_CONFIGS = {
        # as required...
    }
    ```


### Alternative page wrappers

By default `djangocopy/wrapper.html` is used to wrap user content and provide basic settings. You can override this template in
the usual Django way.


### Loading copy without middleware

If you follow the steps above, all views in the project will get access to the copy stored in the djangocopy app and all page visits will be tracked (including admin access).

That carries a small overhead so if you want to avoid that you can instead use the corresponding decorators to each of the views that will require access to the copy content (`@copy_decorator`) and/or
tracking (`@track_decorator`). For example:

    ```
    from django.utils.decorators import decorator_from_middleware
    from djangocopy.middleware import CopyMiddleware

    @copy_decorator
    def my_view
        ...
    ```


### IP Localisation

djangocopy can localise the IP address requesting a page and adapt the output depending on where the request comes from (as well as 
which language is the broser set to).

To enable this functionality, install the database files from Maxmind at https://www.maxmind.com/en/geoip2-databases in a folder of
 your choice and add `GEOIP_PATH` to the settings pointing to that folder 

for example:

    ```
    GEOIP_PATH = BASE_DIR.joinpath('assets', 'geoip')
    ```


## Usage

The `examples` folder contains simple examples and can be used as a template for a new site. A pre-populated sqlite3 database
is included in the distribution but you still need to load the `sample.html` file into the `sample` template for the test
site to work.

Generally, the workflow for creating a new site is to go to the admin panel and then:

1. Create one or more templates in `templates/djangocopy/templates` in your project folders (or you can start with those provided with Djangocopy in the folder of the same name - `simple` and `sample` are provided).
2. Create one or more pages that depend on those templates
3. Populate the copy for those templates (for the sample above create a plaintex entry called `paragraph` and a JSON 
list or strings called `listitems`)
1. Done!

Warning - new templates are only loaded when manage.py migrate is called. A current limitation is that an actual migration must be run for the template upload code to be run

You can go further and setup a navbar as well. the navbar system is fairly complex and allows different user groups 
to see different navbars (which can be combined in a user defined order). Defining a navbar relies on setting up a 
JSON list-of-dicts element with each item in the list containing the various parameters of each navbar entry. Icons 
and dropdowns are supported. the URLs can be relative, absolute or named URLs. Here is a fairly complex example and 
you can find slightly more complex examples in the sqlite3 database that comes with the sample site:

    ```
    [
        {
            "label": "Sample",
            "url": "/djangocopy/sample",
            "faicon": "dashboard"
        },
        {
            "label": "Tools",
            "faicon": "cogs",
            "dropdown": [
                {
                    "label": "Board",
                    "url": "/djangocopy/live"
                },
                {
                    "label": "Pipeline",
                    "url": "/djangocopy/pipeline",
                    "divider": 1
                },
                {
                    "label": "Search",
                    "url": "/djangocopy/clients"
                }
            ]
        }
    ]
    ```


## Open source licenses

This product depends on the following software and media packages

Font Awesome fonts version 4.7 is licensed under [SIL OFL 1.1](http://scripts.sil.org/OFL) and the [MIT License](http://opensource.org/licenses/mit-license.html)

Bootstrap version 4.0 is licensed under the [MIT License](http://opensource.org/licenses/mit-license.html)

GeoLite2 data created by MaxMind, available from [http://www.maxmind.com](http://www.maxmind.com)
