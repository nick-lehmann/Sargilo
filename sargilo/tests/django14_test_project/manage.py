#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
    # try:
    #     execute_from_command_line(sys.argv)
    # except Exception:
    #     from django.conf import settings as django_settings
    #     from raven.contrib.django.models import get_client
    #
    #     if 'raven.contrib.django.raven_compat' not in django_settings.INSTALLED_APPS:
    #         raise
    #
    #     exc_info = sys.exc_info()
    #     if getattr(exc_info[0], 'skip_sentry', False):
    #         raise
    #
    #     get_client().captureException(exc_info)
    #
    #     # Always raise at the end so that the exit code
    #     # is not 0 and the caller gets a proper output on
    #     # the console.
    #     raise
