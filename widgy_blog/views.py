import datetime

from django.utils import six
from django.utils.six.moves.urllib import parse
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.syndication.views import Feed
from django.core import urlresolvers

from widgy.utils import build_url
from widgy.templatetags.widgy_tags import render_root
from widgy.models import Node
from widgy.contrib.form_builder.views import HandleFormMixin

from .models import Blog, BlogLayout, Tag
from .site import site
from .utils import date_list_to_archive_list


class RedirectGetHandleFormMixin(HandleFormMixin):
    """
    A HandleFormMixin that redirects away the `?from=...` URLs for get
    requests.
    """
    def get(self, request, *args, **kwargs):
        from_ = request.GET.get('from')
        if from_:
            return redirect(from_)
        else:
            return super(RedirectGetHandleFormMixin, self).get(request, *args, **kwargs)


class BlogRenderer(object):
    def __init__(self, blog, url_kwargs, request):
        self.blog = blog
        self.url_kwargs = url_kwargs
        root_node_pk = url_kwargs.get('root_node_pk')
        if root_node_pk:
            self.root_node = get_object_or_404(Node, pk=root_node_pk)
        else:
            self.root_node = blog._meta.get_field('content').get_render_node(blog, {'request': request})
            if not self.root_node:
                self.root_node = (blog.content.head and blog.content.head.root_node) or blog.content.working_copy
        self.content = self.root_node.content

    @property
    def title(self):
        return self.content.title

    def get_absolute_url(self):
        return self.blog.get_absolute_url_with_layout(self.content)

    @property
    def slug(self):
        return self.content.slug

    @property
    def date(self):
        return self.blog.date

    def render(self):
        return render_root({'root_node_override': self.root_node}, self.blog, 'content')

    @property
    def has_incorrect_slug(self):
        try:
            return self.slug != self.url_kwargs['slug']
        except KeyError:
            # preview/form submit, slug doesn't matter
            return False


class BlogQuerysetMixin(object):
    model = BlogLayout

    def get_queryset(self):
        return self.get_published_blogs()

    def get_published_blogs(self):
        return self.model.objects.select_related('image').published().order_by('-date')

    def get_archive_years(self, qs):
        return date_list_to_archive_list(qs.values_list('date', flat=True).order_by('-date'))

    def get_context_data(self, **kwargs):
        data = super(BlogQuerysetMixin, self).get_context_data(**kwargs)
        data['blog_archive'] = self.get_archive_years(self.get_published_blogs())
        return data


class BlogListView(BlogQuerysetMixin, ListView):
    context_object_name = 'blog_list'
    template_name = 'widgy/widgy_blog/blog_list.html'
    paginate_by = 10

    def get_canonical_url(self):
        """Determine whether to send a canonical url for the blog list.

        A blog list view without any query should be the same as a blog
        list view with query `page=1`. The `page=1` view should have a canonical
        link to the simpler URL.
        """
        if self.request.GET.get('page') == '1':
            querystring = self.request.GET.copy()
            del querystring['page']
            return parse.urlunsplit(('', '', self.request.path, querystring.urlencode(), ''))
        else:
            return None

    def get_neighbor_pages(self):
        querystring = self.request.GET.copy()
        paginator = self.get_paginator(self.get_queryset(), self.paginate_by)
        page = self.get_current_page(paginator)

        prev_page = None
        next_page = None

        if page.has_previous():
            prev_page = page.previous_page_number()

        if page.has_next():
            next_page = page.next_page_number()

        return {'prev': prev_page, 'next': next_page}

    def get_neighbor_rel_links(self):
        neighbor_pages = self.get_neighbor_pages()
        querystring = self.request.GET.copy()
        prev_link = None
        next_link = None

        if neighbor_pages['prev']:
            if neighbor_pages['prev'] == 1:
                # Link to the canonical url
                del querystring['page']
            else:
                querystring['page'] = neighbor_pages['prev']

            prev_link = build_url(self.request.path, querystring)
        if neighbor_pages['next']:
            querystring['page'] = neighbor_pages['next']
            next_link = build_url(self.request.path, querystring)

        return {'prev_link': prev_link, 'next_link': next_link}

    def get_current_page(self, paginator):
        """Return the current page number.

        Taken from paginate_queryset in ListView."""
        page = self.kwargs.get(self.page_kwarg) or self.request.GET.get(self.page_kwarg) or 1

        try:
            page_num = int(page)
        except ValueError:
            if page == 'last':
                page_num = paginator.num_pages
            else:
                raise Http404("Page is not 'last', nor can it be converted to an int.")

        return paginator.page(page_num)

    def get_context_data(self, **kwargs):
        kwargs = super(BlogListView, self).get_context_data(**kwargs)
        kwargs['tags'] = Tag.objects.all()
        kwargs['canonical_url'] = self.get_canonical_url()
        kwargs.update(self.get_neighbor_rel_links())

        return kwargs


class TagView(BlogListView):
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['tag'])
        return super(TagView, self).get_queryset().filter(tags=self.tag)

    def get_context_data(self, **kwargs):
        kwargs = super(TagView, self).get_context_data(**kwargs)
        kwargs['current_tag'] = self.tag
        return kwargs


class BlogYearArchiveView(BlogListView):
    def get_queryset(self):
        qs = super(BlogYearArchiveView, self).get_queryset()
        return qs.filter(date__year=self.kwargs['year'])

    def get_context_data(self, **kwargs):
        kwargs = super(BlogYearArchiveView, self).get_context_data(**kwargs)
        year = int(self.kwargs['year'])
        kwargs['archive_date'] = datetime.date(year, 1, 1)
        return kwargs


class BlogMonthArchiveView(BlogListView):
    def get_queryset(self):
        qs = super(BlogMonthArchiveView, self).get_queryset()
        return qs.filter(
            date__year=self.kwargs['year'],
            date__month=self.kwargs['month']
        )

    def get_context_data(self, **kwargs):
        kwargs = super(BlogMonthArchiveView, self).get_context_data(**kwargs)
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        kwargs['archive_date'] = datetime.date(year, month, 1)
        return kwargs


class BlogDetailView(BlogQuerysetMixin, RedirectGetHandleFormMixin, DetailView):
    context_object_name = 'blog'
    template_name = 'widgy/widgy_blog/blog_detail.html'
    site = site
    owner_class = Blog

    def get_object(self):
        try:
            # this method is called more than once
            return self.object
        except AttributeError:
            pass

        self.root_node_pk = self.kwargs.get('root_node_pk')

        qs = self.owner_class.objects.filter(
            pk=self.kwargs['pk']
        ).select_related(
            'content__head__root_node',
        )
        if self.root_node_pk:
            self.site.authorize_view(self.request, self)
        else:
            qs = qs.filter(
                content__commits__root_node__content_id__in=self.get_queryset()
            )
        blog = get_object_or_404(qs)

        return BlogRenderer(blog, self.kwargs, self.request)

    def dispatch(self, request, *args, **kwargs):
        self.object = blog = self.get_object()
        if blog.has_incorrect_slug:
            return redirect(blog)
        return super(BlogDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super(BlogDetailView, self).get_context_data(**kwargs)
        kwargs['object'] = self.object
        if hasattr(self, 'form_node'):
            self.object.root_node = self.form_node.get_root()
        # BlogRenderer calculates and fetches this
        kwargs['root_node_override'] = self.object.root_node
        return kwargs


list = BlogListView.as_view()
year_archive = BlogYearArchiveView.as_view()
month_archive = BlogMonthArchiveView.as_view()
detail = BlogDetailView.as_view()
tag = TagView.as_view()


class RssFeed(Feed):
    title = "Blog Feed"
    link = urlresolvers.reverse_lazy('blog_list')
    model = BlogLayout

    def get_object(self, request, tag=None):
        if tag is not None:
            return get_object_or_404(Tag, slug=tag)
        else:
            return None

    def items(self, obj=None):
        qs = self.model.objects.published()
        if obj is not None:
            qs = qs.filter(tags=obj)
        return qs

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        # Instead of this, BlogLayout.date should be a datetime.
        return datetime.datetime.combine(item.date, datetime.time())

    def item_author_name(self, item):
        return item.author.get_full_name()

    def item_description(self, item):
        return item.description


feed = RssFeed()
