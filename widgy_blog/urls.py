from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.list, name='blog_list'),
    re_path(r'^(?P<year>\d{4})/$', views.year_archive, name='blog_archive_year'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', views.month_archive, name='blog_archive_month'),
    re_path(r'^detail/(?P<slug>.+)/(?P<pk>\d+)/$', views.detail, name='blog_detail'),
    re_path(r'^tag/(?P<tag>.+)/$', views.tag, name='blog_tag'),
    re_path(r'^tag/(?P<tag>.+)/feed\.xml$', views.feed, name='blog_tag_rss_feed'),
    re_path(r'^feed\.xml$', views.feed, name='blog_rss_feed'),
    # widgy
    re_path(r'^preview/(?P<pk>\d+)/(?P<root_node_pk>\d+)/$', views.detail, name='blog_detail_preview'),
    re_path(r'^form/(?P<pk>\d+)/(?P<form_node_pk>\d+)/$', views.detail, name='blog_detail_form'),
]
