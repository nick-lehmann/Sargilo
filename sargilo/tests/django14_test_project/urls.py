# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns(
    '',
    # url(r'^app_test/', include('app_test.urls')),
    url(r'^admin/', include(admin.site.urls)))
