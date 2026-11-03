from django.urls import include, path, re_path
from django.contrib import admin


def dummy_view(*args, **kwargs):
    pass


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('widgy_blog.urls')),
    path('widgy-mezzanine/', include('widgy.contrib.widgy_mezzanine.urls')),
    path('mezzanine/', include('mezzanine.urls')),
    # mezzanine.pages.views.page reverses the 'home' url.
    re_path(r'^$', dummy_view, name='home'),
]
