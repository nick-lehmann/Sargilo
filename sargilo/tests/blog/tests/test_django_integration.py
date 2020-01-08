from datetime import date
from unittest import skipIf

from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase

from sargilo.collection import CollectionConfig
from sargilo.relations import (
    IncomingForeignKeyRelation,
    OutgoingForeignKeyRelation,
    ManyToManyRelation
)
from sargilo.integrations.django_integration import DjangoIntegration
from sargilo.tests.blog.models import Post, Tag, Slug, Comment, Critique

from .compatibility import DJANGO_NOT_SUPPORTED, DJANGO_ERROR

try:
    from typing import GenericMeta
except ImportError:
    pass


@skipIf(DJANGO_NOT_SUPPORTED, DJANGO_ERROR)
class DjangoIntegrationTestCase(TestCase):
    def setUp(self):
        self.django_integration = DjangoIntegration()

    def test_basic_creation(self):
        tag_config = CollectionConfig(model=Tag, creation_function=lambda model: model.objects.create)

        sample_tag_data = {
            'name': 'Politics'
        }

        self.django_integration.create_instance(config=tag_config, data=sample_tag_data)

        self.assertEqual(Tag.objects.all().count(), 1)

    def test_post_introspection(self):
        """
        Test more complex model with all types of relations.
        """
        post_configuration = CollectionConfig(model=Post)
        type_mapping = self.django_integration.introspect_collection(post_configuration)

        # TODO: Test m2m relation with no through model
        expected_mapping = {
            'title': str,
            'content': str,
            'publish_date': date,
            'slugs': IncomingForeignKeyRelation[Slug],
            'author': OutgoingForeignKeyRelation[User],
            'tags': ManyToManyRelation[None, Tag],
            'comments': ManyToManyRelation[Comment, User]
        }

        self.maxDiff = 0
        self.assertEqual(type_mapping, expected_mapping)

    @skipIf(DJANGO_NOT_SUPPORTED, DJANGO_ERROR)
    def test_user_introspection(self):
        user_configuration = CollectionConfig(model=User)
        type_mapping = self.django_integration.introspect_collection(user_configuration)

        self.assertEqual(len(type_mapping), 14)

        # Basic types
        self.assertEqual(type_mapping['username'], str)
        self.assertEqual(type_mapping['first_name'], str)
        self.assertEqual(type_mapping['last_name'], str)
        self.assertEqual(type_mapping['email'], str)
        self.assertEqual(type_mapping['password'], str)

        self.assertEqual(type_mapping['is_active'], bool)
        self.assertEqual(type_mapping['is_staff'], bool)
        self.assertEqual(type_mapping['is_superuser'], bool)

        self.assertEqual(type_mapping['date_joined'], date)
        self.assertEqual(type_mapping['last_login'], date)

        # Custom defined relations
        self.assertEqual(type_mapping['posts'], IncomingForeignKeyRelation[Post])
        self.assertEqual(type_mapping['critiques'], IncomingForeignKeyRelation[Critique])

        # Builtin m2m relations without custom through model
        self.assertEqual(type(type_mapping['groups']), GenericMeta)
        self.assertEqual(type_mapping['groups'].__args__[1], Group)

        self.assertEqual(type(type_mapping['user_permissions']), GenericMeta)
        self.assertEqual(type_mapping['user_permissions'].__args__[1], Permission)

