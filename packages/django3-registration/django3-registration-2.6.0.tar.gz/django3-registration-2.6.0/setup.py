# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['registration',
 'registration.backends',
 'registration.backends.default',
 'registration.backends.hmac',
 'registration.backends.model_activation',
 'registration.backends.simple',
 'registration.management',
 'registration.management.commands',
 'registration.migrations',
 'registration.tests']

package_data = \
{'': ['*'],
 'registration': ['locale/ar/LC_MESSAGES/*',
                  'locale/bg/LC_MESSAGES/*',
                  'locale/ca/LC_MESSAGES/*',
                  'locale/cs/LC_MESSAGES/*',
                  'locale/da/LC_MESSAGES/*',
                  'locale/de/LC_MESSAGES/*',
                  'locale/el/LC_MESSAGES/*',
                  'locale/en/LC_MESSAGES/*',
                  'locale/es/LC_MESSAGES/*',
                  'locale/es_AR/LC_MESSAGES/*',
                  'locale/fa/LC_MESSAGES/*',
                  'locale/fr/LC_MESSAGES/*',
                  'locale/he/LC_MESSAGES/*',
                  'locale/hr/LC_MESSAGES/*',
                  'locale/is/LC_MESSAGES/*',
                  'locale/it/LC_MESSAGES/*',
                  'locale/ja/LC_MESSAGES/*',
                  'locale/ko/LC_MESSAGES/*',
                  'locale/nb/LC_MESSAGES/*',
                  'locale/nl/LC_MESSAGES/*',
                  'locale/pl/LC_MESSAGES/*',
                  'locale/pt/LC_MESSAGES/*',
                  'locale/pt_BR/LC_MESSAGES/*',
                  'locale/ru/LC_MESSAGES/*',
                  'locale/sl/LC_MESSAGES/*',
                  'locale/sr/LC_MESSAGES/*',
                  'locale/sv/LC_MESSAGES/*',
                  'locale/tr_TR/LC_MESSAGES/*',
                  'locale/zh_CN/LC_MESSAGES/*',
                  'locale/zh_TW/LC_MESSAGES/*'],
 'registration.tests': ['templates/registration/*']}

install_requires = \
['Django>=3.1,<4.0', 'confusable_homoglyphs>=3.0,<4.0']

setup_kwargs = {
    'name': 'django3-registration',
    'version': '2.6.0',
    'description': 'An extensible user-registration application for Django',
    'long_description': '=====================\nDjango3 Registration\n=====================\n\nThis is an extensible user-registration application for Django.  It\nwas forked of the "2.x" branch of `this project\n<https://github.com/ubernostrum/django-registration/>`_.\n\nThat project completely changed its approach to registrations in version\n3.0.  It eliminated models entirely and made many other big changes.\nConverting an existing 2.x project to 3.0 was proving to be\nprohibitively time consuming, so this fork was created to allow the\nolder approach to work under Python 3 and newer versions of Django.\n\nFull documentation is `available online\n<https://django-registration.readthedocs.io/>`_.\n\nInstallation\n============\n    $ pip install django3-registration\n',
    'author': 'James Bennett',
    'author_email': 'james@b-list.org',
    'maintainer': 'Imagescape',
    'maintainer_email': 'info@imagescape.com',
    'url': 'https://github.com/ImaginaryLandscape/django3-registration',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
