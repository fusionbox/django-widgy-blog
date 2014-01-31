import datetime

from django.views.generic import ListView, DetailView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.syndication.views import Feed
from django.core import urlresolvers

from widgy.templatetags.widgy_tags import render_root
from widgy.models import Node
from widgy.contrib.form_builder.views import HandleFormMixin

from .models import Blog, BlogLayout
from .site import site


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


class Year(list):
    def __init__(self, date, *args, **kwargs):
        super(Year, self).__init__(*args, **kwargs)
        self.date = date

    @property
    def count(self):
        return sum(month.count for month in self)

    def get_absolute_url(self):
        return urlresolvers.reverse('blog_archive_year', kwargs={
            'year': self.date.year,
        })


class Month(list):
    def __init__(self, date, *args, **kwargs):
        super(Month, self).__init__(*args, **kwargs)
        self.date = date

    @property
    def count(self):
        return len(self)

    def get_absolute_url(self):
        return urlresolvers.reverse('blog_archive_month', kwargs={
            'year': self.date.year,
            'month': '{0:02}'.format(self.date.month),
        })


class BlogQuerysetMixin(object):
    model = BlogLayout

    def get_queryset(self):
        return self.get_published_blogs()

    def get_published_blogs(self):
        return self.model.objects.select_related('image').published()

    def get_archive_years(self, qs):
        all_dates = qs.values_list('date', flat=True)
        years = []
        for date in all_dates:
            if not years or date.year != years[-1].date.year:
                years.append(Year(date))

            if not years[-1] or date.month != years[-1][-1].date.month:
                years[-1].append(Month(date))

            years[-1][-1].append(date)
        return years

    def get_context_data(self, **kwargs):
        data = super(BlogQuerysetMixin, self).get_context_data(**kwargs)
        data['blog_archive'] = self.get_archive_years(self.get_published_blogs())
        return data


class BlogListView(BlogQuerysetMixin, ListView):
    context_object_name = 'blog_list'
    template_name = 'widgy/widgy_blog/blog_list.html'
    paginate_by = 10


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


class RssFeed(Feed):
    title = "Blog Feed"
    link = urlresolvers.reverse_lazy('blog_list')
    model = BlogLayout

    def items(self):
        return self.model.objects.published()

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
