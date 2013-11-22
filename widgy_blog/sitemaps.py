from django.contrib.sitemaps import Sitemap
from widgy_blog.models import BlogLayout


class BlogSitemap(Sitemap):
    model = BlogLayout

    def items(self):
        return self.model.objects.published()

    def lastmod(self, obj):
        return obj.date
