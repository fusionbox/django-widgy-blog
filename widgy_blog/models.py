from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.functional import cached_property
from django.conf import settings
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers

from fusionbox.db.models import QuerySetManager

import widgy
from widgy.db.fields import VersionedWidgyField
from widgy.contrib.page_builder.models import DefaultLayout, ImageField

from .site import site


class AbstractBlog(models.Model):
    content = VersionedWidgyField(
        null=False,
        on_delete=models.PROTECT,
        site=site,
        root_choices=[
            'BlogLayout',
        ],
    )

    class Meta:
        verbose_name = 'blog post'
        verbose_name_plural = 'blog posts'
        abstract = True

    @models.permalink
    def get_absolute_url(self):
        # we don't know which version's slug to use, so rely on the
        # automatic redirect
        return ('blog_detail', (), {
            'pk': self.pk, 'slug': 'unkown',
        })

    @models.permalink
    def get_absolute_url_with_layout(self, layout):
        return ('blog_detail', (), {
            'pk': self.pk, 'slug': layout.slug,
        })

    def __unicode__(self):
        layout = self.content.working_copy.content
        return layout.title or 'untitled'

    # for admin
    @property
    def title(self):
        return self.content.working_copy.content.title

    @property
    def author(self):
        return self.content.working_copy.content.author

    def get_action_links(self, root_node):
        url = urlresolvers.reverse('blog_detail_preview', kwargs={
            'pk': self.pk,
            'root_node_pk': root_node.pk,
        })

        return [
            {
                'type': 'preview',
                'text': 'Preview',
                'url': url
            },
        ]

    @models.permalink
    def get_form_action_url(self, form, widgy):
        return ('blog_detail_form', (), {
            'pk': self.pk,
            'form_node_pk': form.node.pk,
        })


class Blog(AbstractBlog):
    pass


class AbstractBlogLayout(DefaultLayout):

    class QuerySet(QuerySet):
        def published(self):
            from django.db.models import Max
            from widgy.models import Node

            # put this query in widgy
            VersionTracker = site.get_version_tracker_model()
            published_commit_ids = VersionTracker.objects.published().annotate(
                max_commit_id=Max('commits__pk'),
            ).filter(
                pk__in=Blog.objects.all().values('content'),
            ).values('max_commit_id')

            # After https://code.djangoproject.com/ticket/20378
            # return BlogLayout.objects.filter(_nodes__versioncommit_pk__in=published_commit_ids)

            published_content_ids = Node.objects.filter(
                versioncommit__pk__in=published_commit_ids,
                content_type=ContentType.objects.get_for_model(self.model, for_concrete_model=False),
            ).values('content_id')

            return self.filter(pk__in=published_content_ids)

    objects = QuerySetManager()

    @property
    def meta_title(self):
        if self.page_title:
            return self.page_title
        else:
            return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(AbstractBlogLayout, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-date']
        abstract = True

    @models.permalink
    def get_absolute_url(self):
        return ('blog_detail', (), {
            'pk': self.owner.pk, 'slug': self.slug,
        })

    @cached_property
    def owner(self):
        from django.contrib.contenttypes.models import ContentType

        return Blog.objects.get(
            content__commits__root_node__content_id=self.pk,
            content__commits__root_node__content_type=ContentType.objects.get_for_model(self))


@widgy.register
class BlogLayout(AbstractBlogLayout):
    title = models.CharField(max_length=1023)
    slug = models.CharField(max_length=255, blank=True)
    date = models.DateField(default=timezone.now)
    image = ImageField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    page_title = models.CharField(max_length=255, blank=True, null=True,
                                  help_text='Will default to the blog title')
    author = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
                               related_name='blog_bloglayout_set')
