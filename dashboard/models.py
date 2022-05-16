from django.conf import settings
from django.db import models
from django.core.validators import FileExtensionValidator
from uuid import uuid4
from .validators import FileValidator, is_excel_file
from pathlib import Path
import os

def revised_naming_counter(filename):
    if Path.exists(Path.joinpath(settings.MEDIA_ROOT, filename)):
        i = 1
        name, ext = os.path.splitext(filename)
        file_format = "{0}_revise{1}{2}"
        while Path.exists(Path.joinpath(settings.MEDIA_ROOT, file_format.format(name, i, ext))):
            i += 1
        return file_format.format(name, i, ext)
    return filename

def excel_dir_path(instance, filename):
    return revised_naming_counter(filename)
class Excel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    file = models.FileField(upload_to=excel_dir_path, validators=[
        FileExtensionValidator(allowed_extensions=('xlsx',), message='File is not an Excel format.'),
        FileValidator(max_size=None, content_types=('application/zip', 'application/xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'), tests=(is_excel_file, )),
    ])
    date_uploaded = models.DateTimeField(auto_now_add=True)
