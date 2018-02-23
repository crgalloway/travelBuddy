from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^main$', views.main),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^travels$', views.travels),
	url(r'^logout$', views.logout),
	url(r'^travels/add$', views.add),
	url(r'^addTrip$', views.addTrip),
	url(r'^travels/destination/(?P<number>\d+)$', views.destination),
	url(r'^join/(?P<number>\d+)$', views.join),
	url(r'^$', views.index),
]