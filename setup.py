# -*- coding: utf-8 -*-

import os

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.md')) as f:
    CHANGES = f.read()

install_requires = [
    'amnesiacms'
]

extras_require = {
    'production': [
        'gunicorn'
    ],
    'development': [
        'pyramid_debugtoolbar'
    ]
}

setup(
    name='amnesiabri',
    version='0.0.1',
    description='amnesia bri',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Julien Cigar',
    author_email='julien@perdition.city',
    url='https://github.com/silenius/amnesia',
    keywords='web wsgi pyramid cms sqlalchemy',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='amnesiabri',
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={
        'paste.app_factory': [
            'main = amnesiabri:main'
        ]
    }

)
