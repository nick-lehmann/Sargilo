from datetime import date

from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase

from .test_configuration import test_configuration, dataset_path
from sargilo.collection import CollectionConfig
from sargilo.dataset import Dataset
from sargilo.relations import (
    IncomingForeignKeyRelation,
    OutgoingForeignKeyRelation,
    ManyToManyRelation
)
from sargilo.integrations.django_integration import DjangoIntegration
from sargilo.tests.blog.models import Post, Tag, Slug, Comment, Critique

from typing import GenericMeta


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

    def test_user_introspection(self):
        user_configuration = CollectionConfig(model=User)
        type_mapping = self.django_integration.introspect_collection(user_configuration)

        self.assertEqual(len(type_mapping), 12)

        # Basic types
        self.assertEqual(type_mapping['username'], str)
        self.assertEqual(type_mapping['first_name'], str)
        self.assertEqual(type_mapping['last_name'], str)
        self.assertEqual(type_mapping['email'], str)
        self.assertEqual(type_mapping['password'], str)

        self.assertEqual(type_mapping['is_active'], bool)
        self.assertEqual(type_mapping['is_staff'], bool)
        self.assertEqual(type_mapping['is_superuser'], bool)

        # Custom defined relations
        self.assertEqual(type_mapping['posts'], IncomingForeignKeyRelation[Post])
        self.assertEqual(type_mapping['critiques'], IncomingForeignKeyRelation[Critique])

        # Builtin m2m relations without custom through model
        self.assertEqual(type(type_mapping['groups']), GenericMeta)
        self.assertEqual(type_mapping['groups'].__args__[1], Group)

        self.assertEqual(type(type_mapping['user_permissions']), GenericMeta)
        self.assertEqual(type_mapping['user_permissions'].__args__[1], Permission)


class CreationTestCase(TestCase):
    def setUp(self):
        self.dataset = Dataset(
            dataset_file=dataset_path,
            config=test_configuration,
            integration=DjangoIntegration()
        )

    def test_basic(self):
        self.dataset.read_dataset()
        self.dataset.create_collections()
        self.dataset.create_objects()

        self.check_correct_model_count()
        self.check_correct_item_anchors()
        self.check_user_creation()
        self.check_post_creation()

    def check_correct_model_count(self):
        """
        Check that the correct amount of each model got created.
        """
        self.assertEqual(User.objects.count(), 6)
        self.assertEqual(Tag.objects.count(), 5)
        self.assertEqual(Post.objects.count(), 3)

    def check_correct_item_anchors(self):
        """
        Check that all item anchors are present
        """
        anchors = self.dataset.items.registry.keys()
        anchors.remove('None')  # TODO: Find out why
        expected_anchors = [
            'Post1', 'Post2', 'Post3',
            'Admin', 'Editor', 'Christoph', 'Axel', 'Mike',
            'TestTag', 'BlueTag'
        ]
        self.assertEqual(sorted(anchors), sorted(expected_anchors))

    def check_user_creation(self):
        """
        Checks the correct creation of all users as specified in the
        dataset file.
        """
        self.check_admin_creation()
        self.check_staff_creation()
        self.check_normal_user_creation()

    def check_admin_creation(self):
        """
        Checks the correct creation of the admin user as specified in the
        dataset file.
        """
        admin = self.dataset.items.get_item('Admin')  # type: User

        self.assertEqual(admin.username, 'Admin')
        self.assertEqual(admin.first_name, 'Ernst')
        self.assertEqual(admin.last_name, 'Haft')
        self.assertEqual(admin.email, 'ernst@mail.de')
        self.assertTrue(admin.check_password('very_secret'))

        self.assertTrue(all([admin.is_staff, admin.is_superuser, admin.is_active]))

        self.assertEqual(admin.posts.count(), 1)
        self.assertEqual(admin.comment_set.count(), 0)

    def check_staff_creation(self):
        """
        Checks the correct creation of a staff user as specified in the
        dataset file.
        """
        staff = self.dataset.items.get_item('Editor')  # type User

        self.assertEqual(staff.username, 'Editor')
        self.assertEqual(staff.first_name, 'Wendy')
        self.assertEqual(staff.last_name, 'Lator')
        self.assertEqual(staff.email, 'wendy@mail.de')
        self.assertTrue(staff.check_password('very_secret'))

        self.assertTrue(staff.is_staff)
        self.assertFalse(staff.is_superuser)
        self.assertTrue(staff.is_active)  # default value

        self.assertEqual(staff.posts.count(), 1)

    def check_normal_user_creation(self):
        """
        Checks the correct creation of a normal user as specified in the
        dataset file.
        """
        christoph = self.dataset.items.get_item('Christoph')

        self.assertEqual(christoph.username, 'christoph_smaul')
        self.assertEqual(christoph.first_name, 'Christoph')
        self.assertEqual(christoph.last_name, 'Smaul')
        self.assertEqual(christoph.email, 'christoph@mail.de')
        self.assertTrue(christoph.check_password('christoph_smaul'))

        self.assertFalse(christoph.is_staff)
        self.assertFalse(christoph.is_superuser)
        self.assertFalse(christoph.is_active)

        self.assertEqual(christoph.posts.count(), 0)
        self.assertEqual(christoph.comment_set.count(), 2)

    def check_post_creation(self):
        post1 = self.dataset.items.get_item('Post1')  # type: Post

        self.assertEqual(post1.title, "Hello world")
        self.assertTrue(post1.content.startswith('Lorem ipsum'))
        self.assertEqual(post1.publish_date, date(2019, 2, 28))

        self.assertEqual(post1.author, self.dataset.items.get_item('Admin'))
        self.assertEqual(post1.tags.count(), 1)
        self.assertEqual(post1.slugs.count(), 2)
        self.assertEqual(post1.comments.count(), 2)
