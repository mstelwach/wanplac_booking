from django.conf.urls import url

from reservation.views import *

app_name = 'reservation'

urlpatterns = [
    url(r'^login', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^list/$', ReservationListView.as_view(), name='list'),
    url(r'^create/$', ReservationCreateView.as_view(), name='create'),
    # url(r'^(?P<pk>[\d]+)/payu/process/$', ReservationPayUPaymentView.as_view(), name='payu-process'),
]
