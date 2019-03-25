from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='message_list'),

    # DEPRECATED
    # url(r'^dm$', views.dm, name='message_dm'),

    url(r'^direct_message/$', views.direct_message, name='message_direct'),
    url(r'^group_message/(?P<threadid>[0-9]+)/$', views.group_message, name='message_group'),

    url(r'^thread/(?P<pk>[0-9]+)/$', views.thread, name='message_thread'),

    url(r'^dm_thread/(?P<recipient>[0-9]+)/$', views.get_dm_thread, name='get_dm_thread'),
]
