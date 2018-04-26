from django.conf.urls import url

from .views import (PhoneBookPersonListView,
                    PhoneBookPersonDetailView,
                    PhoneBookPersonDeleteView,
                    PhoneBookPersonCreateView,
                    PhoneBookPersonUpdateView
                    )


urlpatterns = [
    url(r'^$', PhoneBookPersonListView.as_view(), name='contact_list'),
    url(r'^create/$', PhoneBookPersonCreateView.as_view(), name='contact_create'),
    url(r'^(?P<slug>[\w-]+)/(?P<pk>\d+)/$', PhoneBookPersonDetailView.as_view(), name='contact_detail'),
    url(r'^(?P<slug>[\w-]+)/(?P<pk>\d+)/delete$', PhoneBookPersonDeleteView.as_view(), name='contact_delete'),
    url(r'^(?P<slug>[\w-]+)/(?P<pk>\d+)/edit/$', PhoneBookPersonUpdateView.as_view(), name='contact_update'),

]
