from django.views.generic import ListView, DetailView
from django.shortcuts import redirect, get_object_or_404

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


class BlogQuerysetMixin(object):
    model = BlogLayout

    def get_queryset(self):
        return self.get_published_blogs()

    def get_published_blogs(self):
        return self.model.objects.select_related('image').published()


class BlogListView(BlogQuerysetMixin, ListView):
    context_object_name = 'blog_list'
    template_name = 'widgy/widgy_blog/blog_list.html'


class BlogDetailView(BlogQuerysetMixin, RedirectGetHandleFormMixin, DetailView):
    context_object_name = 'blog'
    template_name = 'widgy/widgy_blog/blog_detail.html'
    site = site

    def get_object(self):
        try:
            # this method is called more than once
            return self.object
        except AttributeError:
            pass

        self.root_node_pk = self.kwargs.get('root_node_pk')

        qs = Blog.objects.filter(
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
detail = BlogDetailView.as_view()
