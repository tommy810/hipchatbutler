from django.conf.urls import url 
from office365 import views

urlpatterns = [
  # The home view ('/tutorial/')
  url(r'^$', views.home, name='home'),
  # Explicit home ('/tutorial/home/')
  url(r'^home/$', views.home, name='home'),
  url(r'^calendars/$', views.events, name='calendars'),
  url(r'^events/$', views.events, name='events'),
  # Redirect to get token ('/tutorial/gettoken/')
  url(r'^gettoken/$', views.gettoken, name='gettoken'),
]