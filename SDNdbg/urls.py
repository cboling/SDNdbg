"""
Copyright (c) 2015 - 2016.  Boling Consulting Solutions , BCSW.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from django.conf.urls import include, url
from django.contrib import admin

"""SDNdbg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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

urlpatterns = [
    # Admin and Authorization
    url(r'^admin/', admin.site.urls),
    url('^', include('django.contrib.auth.urls', namespace='core')),

    # Applications
    url(r'^', include('django_home.urls')),
    url(r'^collector/', include('collector.urls')),
    url(r'^deployment/', include('core.urls-deployment')),
    url(r'^onos/', include('onos.urls')),
    url(r'^openstack/', include('openstack.urls')),

    # TODO: Enable each of the following below when ready or clean them up if they will not be used
    #
    # url(r'^linux/', include('linux.urls')),
    # url(r'^odl/', include('odl.urls')),
    # url(r'^ovs/', include('ovs.urls')),
]
