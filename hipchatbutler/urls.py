from django.conf.urls import url, include
from django.contrib import admin
from office365 import views

urlpatterns = [
    # Invoke the home view in the tutorial app by default
    url(r'^$', views.home, name='home'),
    # Defer any URLS to the /tutorial directory to the tutorial app
    url(r'^office365/', include('office365.urls', namespace='office365')),
    url(r'^admin/', include(admin.site.urls)),
]