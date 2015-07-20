from django.http import HttpRequest
from django.contrib.auth import get_user_model

from haystack import indexes

from widgy.templatetags.widgy_tags import render_root
from widgy.utils import html_to_plaintext

from widgy_blog.models import Blog, BlogLayout

from widgy.signals import widgy_pre_index

User = get_user_model()


def fake_request():
    r = HttpRequest()
    r.user = User()
    return r


class BlogIndex(indexes.SearchIndex, indexes.Indexable):
    title = indexes.CharField()
    text = indexes.CharField(document=True)
    # It's expensive to calculate the url for blogs on the search
    # results page (we'd need to query for the published node), so cache
    # it here.
    get_absolute_url = indexes.CharField()

    def full_prepare(self, *args, **kwargs):
        widgy_pre_index.send(sender=self)
        return super(BlogIndex, self).full_prepare(*args, **kwargs)

    def get_model(self):
        return Blog

    def get_bloglayout_queryset(self):
        return BlogLayout.objects.published()

    def index_queryset(self, using=None):
        published_blog_layouts = self.get_bloglayout_queryset()
        return self.get_model().objects.filter(
            content__commits__root_node__content_id__in=published_blog_layouts
        )

    def prepare(self, obj):
        self.prepared_data = super(BlogIndex, self).prepare(obj)

        request = fake_request()
        node = obj.content.get_published_node(request)
        if node is not None:
            # prepare() has to work on unpublished blogs because haystack
            # filters them out at query time, not index time.
            blog_layout = node.content
            ctx = {
                'request': fake_request(),
                'root_node_override': node,
            }
            html = render_root(ctx, obj, 'content')
            content = [
                html_to_plaintext(html),
                blog_layout.title,
                blog_layout.summary,
            ]

            self.prepared_data['title'] = blog_layout.title
            self.prepared_data['text'] = ' '.join(content)
            self.prepared_data['get_absolute_url'] = obj.get_absolute_url_with_layout(blog_layout)

        return self.prepared_data
