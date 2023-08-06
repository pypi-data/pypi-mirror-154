# django-content-safe-uploader

FileField security validators: FileExtensionValidator, FileContentMatchesWithFileExtensionValidator.

## Install

```
pip install django-content-safe-uploader
```

## Usage

*pro/settings.py*

```
INSTALLED_APPS = [
    ...
    "django_content_safe_uploader",
    ...
]
```

*app/models.py*

```
from django.db import models
from django_content_safe_uploader.validators import FileExtensionValidator
from django_content_safe_uploader.validators import FileContentMatchesWithFileExtensionValidator
from django_content_safe_uploader.validators import IMAGE_EXTENSIONS

class Book(models.Model):
    title = models.CharField(max_length=128)
    preview = models.FileField(
        upload_to="book_previews",
        validators=[
            FileExtensionValidator(*IMAGE_EXTENSIONS),
            FileContentMatchesWithFileExtensionValidator(lax_extensions=[IMAGE_EXTENSIONS]),
        ])
```

## Release

### v0.1.0

- First release.
