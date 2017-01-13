"""test_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

import debug_toolbar


urlpatterns = [
    url(r'^$', RedirectView.as_view(
        url=reverse_lazy('stentor:subscriber.subscribe')
    )),

    url(r'^', include('stentor.urls.public', namespace='stentor')),
    url(r'^', include('stentor.urls.private', namespace='stentor')),

    url(r'^admin/', admin.site.urls),

    url(r'^__debug__/', include(debug_toolbar.urls)),
]
