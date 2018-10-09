# django-copy

Probably the smallest and simplest CMS for Django.

While it is extremely simple, it supports some features that I haven't found in other CMS frameworks out there. Namely you can create pages for **multiple languages** but also for **multiple locations** or any conbination of both


## Installation

1. Use pip to instal the latest stable release

    ```
    pip install django-copy
    ```

    You can also install a local copy by running `setup.py install` at the top directory of django-copy


2. Add `cms` to `INSTALLED_APPS` in the project settings

3. Setup `CMS_TEMPLATE_ROOT` to define where uploaded templates are stored. For example:

    ```
    CMS_TEMPLATE_ROOT = 'templates'
    ```

    the above settings will upload templates to `MEDIA_ROOT/templates`

4. Add the  media folder to the `DIRS` list in `TEMPLATES` in order to serve uploaded templates. For example (if `CMS_TEMPLATE_ROOT` is set as above and `BASE_DIR` points to the project root folder):

    ```
    TEMPLATES = [
        {
            ...
            'DIRS': ['media/'],
            ...
        },
    ]
    ````

5. Add `cms.middleware.LocalisationMiddleware` to `MIDDLEWARE` in the project settings file (OR see alternative below)

6. If not set already, set `MEDIA_ROOT` and `MEDIA_URL` in settings


### Optional:

If you follow step 6 above, all views in the project will get access to the content stored in the cms app. That carries a small overhead so if you want to avoid that you can instead add `@decorator_from_middleware(LocalisationMiddleware)` to each of the views that will require access to DB stored content.

For example:

```
from django.utils.decorators import decorator_from_middleware
from cms.middleware import LocalisationMiddleware

@decorator_from_middleware(LocalisationMiddleware)
def my_view
    ...
```

If you are going to use Django's native user authorisations framework add the following to the project `urls.py`:

    ```
    path('accounts/', include('django.contrib.auth.urls')),
    ```

Then setup `LOGIN_URL`, `LOGIN_REDIRECT_URL` and `LOGOUT_REDIRECT_URL`. For example:

    ```
    LOGIN_URL = '/accounts/login'
    LOGIN_REDIRECT_URL = '/'
    LOGOUT_REDIRECT_URL = '/accounts/login'
    ```


## Open source licenses

This product includes the following software and media packages

GeoLite2 data created by MaxMind, available from [http://www.maxmind.com](http://www.maxmind.com)

Font Awesome fonts version 4.7 is licensed under [SIL OFL 1.1](http://scripts.sil.org/OFL) and the [MIT License](http://opensource.org/licenses/mit-license.html)

Bootstrap version 4.0

