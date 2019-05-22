# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault(b'DJANGO_SETTINGS_MODULE', b'testproject.settings')

application = get_wsgi_application()
