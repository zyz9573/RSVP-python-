from django.conf.urls import url
from . import views

app_name = 'event'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(),name='index'),
    url(r'^(?P<pk>[0-9]+)/$',views.DetailView.as_view(),name='detail'),
    url(r'^(?P<event_id>[0-9]+)/answer/$',views.answer,name='answer'),
    url(r'event/add/$',views.EventCreate.as_view(),name='event-add'),
    url(r'event/(?P<pk>[0-9]+)/$',views.EventUpdate.as_view(),name='event-update'),
    url(r'event/(?P<pk>[0-9]+)/delete/$',views.EventDelete.as_view(),name='event-delete'),

]

