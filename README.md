# django-copy

Probably the smallest and simplest CMS for Django.

While it is extremely simple, it supports some features that I haven't found in other CMS frameworks. Namely you can create 
pages for multiple languages but also for multiple locations or any conbination of both.


## Usage


## Installation

1. Use pip to instal the latest stable release

    ```
    pip install django-copy
    ```

    You can also install a local copy by running `setup.py install` at the top directory of django-copy


2. Add `djangocopy` and it's dependencies to `INSTALLED_APPS` in the project settings (see dependencies below)

    ```
    'ckeditor',
    'ckeditor_uploader',
    'filer'
    'easy_thumbnails',
    'simple_history',
    'djangocopy',
    ```

5. Add `djangocopy.middleware.LocalisationMiddleware` to `MIDDLEWARE` in the project settings file 
(OR see alternative further below)


## Configuration

1. If not set already, set `MEDIA_ROOT` and `MEDIA_URL` in settings. For example:

    ```
    MEDIA_ROOT = BASE_DIR.joinpath('media')
    MEDIA_URL = '/media/'
    ```

2. Also in settings, create `DJANGOCOPY_TEMPLATES` and `DJANGOCOPY_IMAGES` to define where uploaded template and imagefiles are 
stored. These paths will sit below `MEDIA_ROOT` so add the media folder to the `DIRS` list in `TEMPLATES` to make it searchable 
by the Django template framework. For example:

    ```
    DJANGOCOPY_TEMPLATES = 'copy/templates/'
    DJANGOCOPY_IMAGES = 'copy/images/'
    TEMPLATES[0]['DIRS'] += [MEDIA_ROOT]
    ```


7. In _urls.py_ add

    ```
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('filer/', include('filer.urls')),
    path('djangocopy/', include('djangocopy.urls')),
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


## Optional

#### Alternative page wrappers

By default `djangocopy/wrapper.html` is used to wrap user content and provide basic settings. You can override this template in
the usual Django way.


#### Localisation Middleware

If you follow the steps above, all views in the project will get access to the content stored in the djangocopy app. That carries 
a small overhead so if you want to avoid that you can instead add `@decorator_from_middleware(LocalisationMiddleware)` to each of 
the views that will require access to DB stored content. For example:

    ```
    from django.utils.decorators import decorator_from_middleware
    from djangocopy.middleware import LocalisationMiddleware

    @decorator_from_middleware(LocalisationMiddleware)
    def my_view
        ...
    ```


#### IP Localisation

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

1. Create one or more templates (you can start with `djangocopy/templates/sample.html` as in the exmaple provided)
2. Create one or more pages that depend on those templates
3. Populate the copy for those templates (for the sample above create a plaintex entry called `paragraph` and a JSON 
list or strings called `listitems`)
4. Done!

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
