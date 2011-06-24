from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^avalon/', include('avalon.foo.urls')),

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^polls/$', 'avalon.polls.views.index'),
    (r'^polls/(?P<poll_id>\d+)/$', 'avalon.polls.views.detail'),
    (r'^polls/(?P<poll_id>\d+)/results/$', 'avalon.polls.views.results'),
    (r'^polls/(?P<poll_id>\d+)/vote/$', 'avalon.polls.views.vote'),
)
