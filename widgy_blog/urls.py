from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list, name='blog_list'),
    url(r'^(?P<year>\d{4})/$', views.year_archive, name='blog_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', views.month_archive, name='blog_archive_month'),
    url(r'^detail/(?P<slug>.+)/(?P<pk>\d+)/$', views.detail, name='blog_detail'),
    url(r'^tag/(?P<tag>.+)/$', views.tag, name='blog_tag'),
    url(r'^tag/?(P<tag>.+)/feed\.xml$', views.feed, name='blog_rss_feed'),
    url(r'^feed\.xml$', views.feed, name='blog_rss_feed'),
    # widgy
    url(r'^preview/(?P<pk>\d+)/(?P<root_node_pk>\d+)/$', views.detail, name='blog_detail_preview'),
    url(r'^form/(?P<pk>\d+)/(?P<form_node_pk>\d+)/$', views.detail, name='blog_detail_form'),
]
