# Squashed replacement for the 2015 migration history, generated from the
# models as of the Django 4.2 upgrade. Databases that already applied the
# original migrations (listed in ``replaces``) will skip this one.
#
# The data migration in 0002 (a timezone adjustment for ``date``) is not
# carried over: it only ever mattered for rows created before mid-2015.

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields
import widgy.contrib.page_builder.db.fields
import widgy.db.fields
import widgy.models.mixins


class Migration(migrations.Migration):

    initial = True

    replaces = [
        ("widgy_blog", "0001_initial"),
        ("widgy_blog", "0002_auto_20150617_1302"),
        ("widgy_blog", "0003_auto_20150701_1432"),
        ("widgy_blog", "0004_auto_20150710_1604"),
        ("widgy_blog", "0005_auto_20150722_1048"),
    ]

    dependencies = [
        ("widgy", "0002_alter_versiontracker_head_and_more"),
        ("filer", "0018_alter_file_options"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True, editable=False, populate_from="name", unique=True
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BlogLayout",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=1023)),
                ("date", models.DateTimeField(default=django.utils.timezone.now)),
                ("summary", models.TextField(blank=True, null=True)),
                (
                    "slug",
                    models.CharField(
                        blank=True,
                        help_text="Will default to the blog title",
                        max_length=255,
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
                ("keywords", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "page_title",
                    models.CharField(
                        blank=True,
                        help_text="Will default to the blog title",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="blog_bloglayout_set",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "image",
                    widgy.contrib.page_builder.db.fields.ImageField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="filer.file",
                    ),
                ),
                ("tags", models.ManyToManyField(blank=True, to="widgy_blog.tag")),
            ],
            options={
                "ordering": ["-date"],
                "abstract": False,
            },
            bases=(widgy.models.mixins.StrictDefaultChildrenMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "content",
                    widgy.db.fields.VersionedWidgyField(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="widgy.versiontracker",
                    ),
                ),
            ],
            options={
                "verbose_name": "blog post",
                "verbose_name_plural": "blog posts",
            },
        ),
    ]
