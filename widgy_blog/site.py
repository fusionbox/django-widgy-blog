from django.conf import settings

from widgy.utils import fancy_import

site = fancy_import(settings.WIDGY_MEZZANINE_SITE)
