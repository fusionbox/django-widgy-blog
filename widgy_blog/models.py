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


class Blog(models.Model):
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

    @models.permalink
    def get_absolute_url(self):
        # we don't know which version's slug to use, so rely on the
        # automatic redirect
        return ('widgy_blog.views.detail', (), {
            'pk': self.pk, 'slug': 'unkown',
        })

    @models.permalink
    def get_absolute_url_with_layout(self, layout):
        return ('widgy_blog.views.detail', (), {
            'pk': self.pk, 'slug': layout.slug,
        })

    def __unicode__(self):
        layout = self.content.working_copy.content
        return layout.title or 'untitled'

    # for admin
    def title(self):
        return self.content.working_copy.content.title

    def author(self):
        return self.content.working_copy.content.author

    def get_action_links(self, root_node):
        url = urlresolvers.reverse('widgy_blog.views.detail', kwargs={
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
        return ('widgy_blog.views.detail', (), {
            'pk': self.pk,
            'form_node_pk': form.node.pk,
        })


@widgy.register
class BlogLayout(DefaultLayout):
    title = models.CharField(max_length=1023)
    slug = models.CharField(max_length=255, blank=True)
    date = models.DateField(default=timezone.now)
    author = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
                               related_name='blog_bloglayout_set')
    image = ImageField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)

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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(BlogLayout, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-date']

    @models.permalink
    def get_absolute_url(self):
        return ('widgy_blog.views.detail', (), {
            'pk': self.owner.pk, 'slug': self.slug,
        })

    @cached_property
    def owner(self):
        from django.contrib.contenttypes.models import ContentType

        return Blog.objects.get(
            content__commits__root_node__content_id=self.pk,
            content__commits__root_node__content_type=ContentType.objects.get_for_model(self))
