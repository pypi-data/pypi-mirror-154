# -*- coding: utf-8 -*-
import os
import sys
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, 'requirements.txt'), "r", encoding="utf-8") as fobj:
    requires = [x.strip() for x in fobj.readlines() if x.strip()]

setup(
    name="django-content-safe-uploader",
    version="0.1.0",
    description="FileField security validators: FileExtensionValidator, FileContentMatchesWithFileExtensionValidator.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="zencore",
    author_email="dobetter@zencore.cn",
    license="MIT",
    license_files=("LICENSE",),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords=["django", "django admin", "django filefield", "libmagic", "puremagic", "file command"],
    install_requires=requires,
    packages=find_packages(".", exclude=[
        "django_content_safe_uploader",
        "django_content_safe_uploader_example",
        "django_content_safe_uploader_example.migrations",
        ]),
    include_package_data=True,
    zip_safe=False,
)
