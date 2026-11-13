from django.conf import settings
from django.utils.module_loading import import_string

site = import_string(settings.WIDGY_MEZZANINE_SITE)
