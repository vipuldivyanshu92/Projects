from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^blog/', include('blog.foo.urls')),
    (r'^article/$', 'blog.article.views.index'),
    (r'^article/page/$', 'blog.article.views.page'),
    (r'^article/page/(?P<pID>\d+)/$', 'blog.article.views.page'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
)
