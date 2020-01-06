#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

if __name__ == '__main__':
    os.environ.setdefault(b'DJANGO_SETTINGS_MODULE', b'settings')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
