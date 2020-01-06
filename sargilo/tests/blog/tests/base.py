import json
from datetime import date
from unittest import skipIf

from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase

from .test_configuration import test_configuration, dataset_path, schema_path
from sargilo.collection import CollectionConfig
from sargilo.dataset import Dataset
from sargilo.relations import (
    IncomingForeignKeyRelation,
    OutgoingForeignKeyRelation,
    ManyToManyRelation
)
from sargilo.integrations.django_integration import DjangoIntegration
from sargilo.schema import JSONSchema
from sargilo.tests.blog.models import Post, Tag, Slug, Comment, Critique

import django

try:
    from typing import GenericMeta
except ImportError:
    pass

DJANGO_VERSION = django.get_version()
DJANGO_VERSION_PARTS = list(map(int, DJANGO_VERSION.split('.')))
DJANGO_NOT_SUPPORTED = (
        DJANGO_VERSION_PARTS[0] > 1 or
        DJANGO_VERSION_PARTS[0] == 1 and DJANGO_VERSION_PARTS[1] > 7
)
DJANGO_ERROR = 'Django version {} is currently not supported'.format(DJANGO_VERSION)
