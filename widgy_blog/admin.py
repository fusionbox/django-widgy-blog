from functools import partial

from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import modelform_factory
from django.contrib.admin.views.main import ChangeList
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model

from widgy.admin import WidgyAdmin
from widgy.forms import WidgyForm
from widgy.models import Node

from .models import Blog, BlogLayout, Tag

User = get_user_model()


class IsPublishedListFilter(admin.SimpleListFilter):
    title = 'Published'
    parameter_name = 'is_published'
    model = BlogLayout

    def lookups(self, request, model_admin):
        return (
            ('0', 'No'),
            ('1', 'Yes'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.exclude(
                content__commits__root_node__content_id__in=self.model.objects.published()
            ).distinct()
        if self.value() == '1':
            return queryset.filter(
                content__commits__root_node__content_id__in=self.model.objects.published()
            ).distinct()


class AuthorListFilter(admin.SimpleListFilter):
    title = 'Current author'
    parameter_name = 'author'

    def lookups(self, request, model_admin):
        for user in User.objects.filter(blog_bloglayout_set__isnull=False).distinct():
            yield (str(user.pk), str(user))

    def queryset(self, request, queryset):
        pk = self.value()
        if pk:
            layouts_by_this_author = BlogLayout.objects.filter(author__pk=pk)
            return queryset.filter(
                content__working_copy__content_id__in=layouts_by_this_author
            ).distinct()


class BlogForm(WidgyForm):
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')

        if instance:
            try:
                content = instance.content.working_copy.content
            except ObjectDoesNotExist:
                pass
            else:
                opts = self._meta
                initial = model_to_dict(content, opts.fields, opts.exclude)
                initial.update(kwargs.get('initial', {}))
                kwargs['initial'] = initial
        super(BlogForm, self).__init__(*args, **kwargs)


class BlogChangeList(ChangeList):
    def get_results(self, request):
        super(BlogChangeList, self).get_results(request)
        # This is like prefetch_related, but works with our GenericForeignKey
        Node.attach_content_instances(i.content.working_copy for i in self.result_list)


class BlogAdmin(WidgyAdmin):
    form = BlogForm
    layout_model = BlogLayout
    # These are the fields that are actually stored in widgy, not the
    # owner. We copy them back and forth to make the editing interface
    # nicer.
    layout_proxy_fields = [
        'title',
        'slug',
        'date',
        'author',
        'image',
        'summary',
        'description',
        'keywords',
        'page_title',
        'tags',
    ]
    list_filter = [IsPublishedListFilter, AuthorListFilter]
    list_display = ['title', 'author']

    fieldsets = [
        (None, {
            'fields': [
                'title', 'date', 'author', 'image', 'summary', 'content', 'tags',
            ],
        }),
        ('Meta', {
            'fields': ['description', 'keywords', 'slug', 'page_title'],
            'classes': ['collapse', 'grp-collapse', 'collapse-closed',
                        'collapsed'],
        }),
    ]

    def get_queryset(self, request):
        return self.model.objects.select_related('content__working_copy')
    queryset = get_queryset

    def get_changelist(self, *args, **kwargs):
        return BlogChangeList

    def get_form(self, request, obj=None, **kwargs):
        # We need to get the fields for BlogLayout
        defaults = {
            'formfield_callback': partial(self.formfield_for_dbfield, request=request),
            'form': self.form,
            'fields': self.layout_proxy_fields,
        }
        defaults.update(kwargs)
        LayoutModelForm = modelform_factory(self.layout_model, **defaults)
        LayoutForm = type('BlogLayoutForm', (self.form,), LayoutModelForm.base_fields)
        LayoutForm.layout_proxy_fields = self.layout_proxy_fields

        kwargs['form'] = LayoutForm

        return super(BlogAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        layout_data = dict(
            (k, v) for k, v in form.cleaned_data.items() if k in self.layout_proxy_fields
        )
        if not change:
            # adding
            tags = layout_data.pop('tags', [])
            field = self.model._meta.get_field('content')
            obj.content = field.add_root(obj, layout_data)
            obj.content.working_copy.content.tags = tags
        else:
            # editing
            content = obj.content.working_copy.content
            for field_name, value in layout_data.items():
                setattr(content, field_name, value)
            content.save()

        return super(BlogAdmin, self).save_model(request, obj, form, change)

admin.site.register(Blog, BlogAdmin)
admin.site.register(Tag, admin.ModelAdmin)
