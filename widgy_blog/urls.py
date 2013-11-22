from django.conf.urls import patterns, url

urlpatterns = patterns('widgy_blog.views',
    url(r'^$', 'list', name='blog_list'),
    url(r'^(?P<year>\d{4})/$', 'year_archive', name='blog_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'month_archive', name='blog_archive_month'),
    url(r'^detail/(?P<slug>.+)/(?P<pk>\d+)/$', 'detail', name='blog_detail'),
    url(r'^feed\.xml$', 'feed', name='blog_rss_feed'),
    # widgy
    url(r'^preview/(?P<pk>\d+)/(?P<root_node_pk>\d+)/$', 'detail', name='blog_detail_preview'),
    url(r'^form/(?P<pk>\d+)/(?P<form_node_pk>\d+)/$', 'detail', name='blog_detail_form'),
)
