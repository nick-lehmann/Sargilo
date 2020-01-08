import json
from unittest import skipIf

from django.contrib.auth.models import User
from django.test import TestCase

from sargilo.dataset import Dataset
from sargilo.integrations.django_integration import DjangoIntegration
from sargilo.schema import JSONSchema

from .compatibility import DJANGO_NOT_SUPPORTED, DJANGO_ERROR
from .test_configuration import test_configuration, dataset_path, schema_path

try:
    from typing import GenericMeta
except ImportError:
    pass


@skipIf(DJANGO_NOT_SUPPORTED, DJANGO_ERROR)
@skipIf(True, '')  # TODO: Fix tests
class SchemaTestCase(TestCase):
    def setUp(self):
        self.dataset = Dataset(
            dataset_file=dataset_path,
            config=test_configuration,
            integration=DjangoIntegration()
        )
        self.dataset.read_dataset()
        self.dataset.create_collections()
        self.schema = JSONSchema(integration=DjangoIntegration())

    # TODO: Implement requirements
    def test_single_definition_without_requirements(self):
        expected_definition = """
        {
            "type":"object",
            "properties":{
                "username":{"type":"string"},
                "first_name":{"type":"string"},
                "last_name":{"type":"string"},
                "posts":{
                    "type":"array",
                    "items":{
                        "$ref":"#/definitions/post"
                    }
                },
                "critiques":{
                    "type":"array",
                    "items":{
                        "$ref":"#/definitions/critique"
                    }
                },
                "is_active":{"type":"boolean"},
                "is_superuser":{"type":"boolean"},
                "is_staff":{"type":"boolean"},
                "password":{"type":"string"},
                "email":{"type":"string"}
           }
        }
        """
        expected_definition_dict = json.loads(expected_definition)

        user_collection = self.dataset.find_collection_by_model(User)
        generated_definition_dict = self.schema.create_definition(self.type_mappings.get(user_collection))

        self.assertEqual(generated_definition_dict, expected_definition_dict)

    def test_single_list_creation(self):
        schema = JSONSchema(integration=DjangoIntegration())
        expected_list = """
        {
            "type": "array",
            "items": {
                "$ref": "#/definitions/user"
            }
        }
        """

        expected_list_dict = json.loads(expected_list)

        user_collection = self.dataset.find_collection_by_model(User)
        generated_list = schema.create_list(user_collection)

        self.assertEqual(expected_list_dict, generated_list)

    def test_schema_generation(self):
        schema = JSONSchema(integration=DjangoIntegration())

        expected_schema = json.load(open(schema_path))
        generated_schema = schema.generate()

        self.maxDiff = None

        self.assertEqual(expected_schema, generated_schema)


