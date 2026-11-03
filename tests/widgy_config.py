from widgy.site import WidgySite
from widgy.db.fields import VersionedWidgyField, WidgyField


widgy_site = WidgySite()

# Mirrors django-widgy's tests/core_tests/widgy_config.py: the fields have to
# be instantiated once with the dotted path so widgy can resolve the site.
VersionedWidgyField(site='tests.widgy_config.widgy_site')
WidgyField(site='tests.widgy_config.widgy_site')
