from django.conf.urls import patterns, url

urlpatterns = patterns('widgy_blog.views',
    url(r'^$', 'list'),
    url(r'^detail/(?P<slug>.+)/(?P<pk>\d+)/$', 'detail'),
    # widgy
    url(r'^preview/(?P<pk>\d+)/(?P<root_node_pk>\d+)/$', 'detail', name='blog_detail_preview'),
    url(r'^form/(?P<pk>\d+)/(?P<form_node_pk>\d+)/$', 'detail', name='blog_detail_form'),
)
