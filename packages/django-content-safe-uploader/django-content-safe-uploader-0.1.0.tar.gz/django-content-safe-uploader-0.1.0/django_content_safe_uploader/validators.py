
import os

from django.utils.translation import gettext_lazy as _
from django.forms import ValidationError

from simplemagic import file_content_matches_with_file_extension_test
from simplemagic.magic import MAGIC_CONTENT_LENGTH
from simplemagic.magic import IMAGE_EXTENSIONS

class FileExtensionValidator(object):

    def __init__(self, *allowed_extensions):
        self.allowed_extensions = [x.lower() for x in allowed_extensions]
        self.allowed_extensions_display = ", ".join(self.allowed_extensions)

    def __call__(self, file):
        ext = os.path.splitext(file.name)[1]
        if not ext in self.allowed_extensions:
            raise ValidationError(_("{allowed_extensions_display} files only...").format(
                allowed_extensions_display=self.allowed_extensions_display,
            ))

class FileContentMatchesWithFileExtensionValidator(object):

    def __init__(self,
            enable_using_magic=True,
            enable_using_file_command=True,
            enable_using_puremagic=True,
            magic_content_length=None,
            lax_extensions=None,
            ):
        self.enable_using_magic = enable_using_magic
        self.enable_using_file_command = enable_using_file_command
        self.enable_using_puremagic = enable_using_puremagic
        self.magic_content_length = magic_content_length or MAGIC_CONTENT_LENGTH
        self.lax_extensions = lax_extensions or []

    def __call__(self, file):
        result, ext, mimetype = file_content_matches_with_file_extension_test(
            file.name,
            file,
            enable_using_magic=self.enable_using_magic,
            enable_using_file_command=self.enable_using_file_command,
            enable_using_puremagic=self.enable_using_puremagic,
            magic_content_length=self.magic_content_length,
            lax_extensions=self.lax_extensions,
            )
        if not result:
            raise ValidationError(_("The file content is NOT matches with the file extension. The file extension {ext} is NOT in the candinate extensions of file {mimetype}...").format(
                ext=ext,
                mimetype=mimetype,
            ))

