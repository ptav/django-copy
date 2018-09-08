# django-copy

A very simple Content Management System for Django


## Installation

Run `pip install django-copy` for installing the latest stable release

You can also install a local copy by running `setup.py install` at the top
directory of django-simplecrud


## Usage

1. Add `'copy'` to `INSTALLED_APPS` in the project settings file 
2. Add `path('accounts/', include('django.contrib.auth.urls')),` to the `urls.py`
3. Add `cms.middleware.LocalisationMiddleware` to `MIDDLEWARE` in the project settings file (OR see alternative below)


### Optional:

If you follow step (3) above all views in the project will get access to the content stored in the cms app. That carries a small overhead so if you want to avoid that you can instead add `@decorator_from_middleware(LocalisationMiddleware)` to each of the views that will require access to DB stored content.

For example:

```
from django.utils.decorators import decorator_from_middleware
from cms.middleware import LocalisationMiddleware

@decorator_from_middleware(LocalisationMiddleware)
def my_view
    ...
```


## Open source licenses

This product includes GeoLite2 data created by MaxMind, available from [http://www.maxmind.com](http://www.maxmind.com)
