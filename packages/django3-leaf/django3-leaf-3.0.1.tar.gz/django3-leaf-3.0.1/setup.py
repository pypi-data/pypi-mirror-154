# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leaf', 'leaf.migrations', 'leaf.tests']

package_data = \
{'': ['*'], 'leaf': ['static/leaf/css/*']}

install_requires = \
['django-mptt>=0.11.0', 'six>=1.16.0']

setup_kwargs = {
    'name': 'django3-leaf',
    'version': '3.0.1',
    'description': 'Render and serve django templates based on URL.',
    'long_description': '# django3-leaf\n\n> Forked from https://github.com/coremke/django-leaf to provide django 3+ support. Render django templates based on URL path.\n\n[![Build Status](https://img.shields.io/travis/gsmke/django-leaf/master.svg?style=flat)](https://travis-ci.org/gsmke/django-leaf)\n[![Latest Version](https://img.shields.io/pypi/v/django-leaf.svg?style=flat)](https://pypi.python.org/pypi/django-leaf/)\n\n## Quick start\n\n1. Install the package from pypi:\n\n    ```bash\n    pip install django3-leaf\n    ```\n\n2. Add "leaf" and "mptt" to your INSTALLED_APPS:\n\n    ```python\n    INSTALLED_APPS = (\n        ...\n        \'leaf\',\n        \'mptt\',\n    )\n    ```\n\n3. Add leaf urls to *the end* of your urlpatterns:\n\n    ```python\n    url(r\'^\', include(\'leaf.urls\')),\n    ```\n\n## Usage\n\ndjango-leaf can be used to render both "static" and database-backed templates.\n\n### Static Templates\n\nIf you want to render a template when a user goes to `/example/url/`, create one of the following files:\n\n1. example/url.html\n2. example/url/index.html\n3. pages/example/url.html\n4. pages/example/url/index.html\n\n### Database Backed Templates\n\nAfter installing django-leaf, the admin interface will have a new section called `Pages` where you\'ll be able to create your page hierarchy.\n\nTo define your own page model, you need to extend from `leaf.models.Page`.\nThere are a few fields available for customization:\n\n1. **identifier**: A unique identifier for your model. This will be used to associate page nodes with your page implementation. If you don\'t provide an `identifier`, one will be provided for you.\n2. **template**: The template to render.\n3. **admin_page_inline**: The admin class to use when rendering the template fields inline. This defaults to the default ``admin.StackedInline``.\n4. **admin_inlines**: A list of other inlines to add to the admin.\n\nHere\'s an example for creating a page with translations provided by [django-parler](https://github.com/edoburu/django-parler):\n\n```python\n# admin.py\nfrom parler.admin import TranslatableStackedInline\n\n\nclass AboutPageInline(TranslatableStackedInline):\n    pass\n\n# models.py\nfrom django.db import models\nfrom leaf.models import Page\nfrom parler.models import TranslatableModel, TranslatedFields\n\nfrom .admin import AboutPageInline\n\n\nclass AboutPage(Page, TranslatableModel):\n    admin_page_inline = AboutPageInline\n    identifier = \'about-page\'\n    template = "about.html"\n\n    translations = TranslatedFields(\n        headline=models.CharField(max_length=255),\n        copy=models.TextField(blank=True)\n    )\n\n    def __unicode__(self):\n        return self.headline\n```\n\nWhen rendering the template, all of the model fields will be available on the ``page`` context variable:\n\n```django\n{{ page.headline }}\n{{ page.copy }}\n```\n\n#### Home Page\n\nThe root page can be added to django-leaf by adding a new page with `slug=home` and `parent=None`. All pages added under that will be added without the ``home`` part in the path.\n\n# TODO\n\n1. Better documentation.\n2. More configuration options.\n',
    'author': 'Ryan Senkbeil',
    'author_email': 'sysadmin@corecreative.com',
    'maintainer': 'Imagescape',
    'maintainer_email': 'info@imagescape.com',
    'url': 'https://github.com/ImaginaryLandscape/django3-leaf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
