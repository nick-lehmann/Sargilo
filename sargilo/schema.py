from datetime import date, datetime, time
from typing import List

from sargilo.integrations.base import Integration
from sargilo.relations import (
    IncomingForeignKeyRelation,
    OutgoingForeignKeyRelation,
    ManyToManyRelation
)

try:
    from django.db.models import get_models
except ImportError:
    pass


class JSONSchema:
    # TODO: Implement requirements for each collection
    # TODO: Add validators to schema (e.g. minimum number for integers)
    def __init__(self, integration, models=None):
        # type: (Integration, List[object]) -> JSONSchema
        self.models = models if models else get_models()
        self.integration = integration

        self.definitions = dict()
        self.top_level_properties = dict()

    def generate(self):
        for model in self.models:
            self.definitions[self.get_definition_name(model)] = self.create_definition(self.integration.introspect_collection(model=model))

            for expected_name in self.integration.model_to_collection_names(model):
                self.top_level_properties[u'{}'.format(expected_name)] = self.create_list(model)

        return {
            u'$schema': u'http://json-schema.org/draft-07/schema#',
            u'$id': u'example.com/test_schema',
            u'title': u'Test schema',
            u'type': u'object',
            u'definitions': self.definitions,
            u'properties': self.top_level_properties
        }

    def create_definition(self, type_mapping):
        # type: (TypeMapping) -> dict
        properties = dict()

        for key, expected_type in type_mapping.items():
            key = u'{}'.format(key)
            if expected_type is str:
                properties[key] = {
                    u'type': u'string'
                }
            if expected_type is int:
                properties[key] = {
                    u'type': u'integer'
                }

            if expected_type is date:
                # TODO: Add format validator
                properties[key] = {
                    u'type': u'string'
                }

            if expected_type is bool:
                properties[key] = {
                    u'type': u'boolean'
                }

            if issubclass(expected_type, OutgoingForeignKeyRelation):
                definition_name = self.get_definition_name(expected_type.__args__[0])

                if not definition_name:
                    continue

                properties[key] = {
                    u'$ref': u'#/definitions/{}'.format(definition_name)
                }

            if issubclass(expected_type, IncomingForeignKeyRelation):
                definition_name = self.get_definition_name(expected_type.__args__[0])

                if not definition_name:
                    continue

                properties[key] = {
                    u'type': u'array',
                    u'items': {
                        u'$ref': u'#/definitions/{}'.format(definition_name)
                    }
                }

            if issubclass(expected_type, ManyToManyRelation):
                through_model, referenced_model = expected_type.__args__

                if through_model is not type(None):
                    definition_name = self.get_definition_name(through_model)
                else:
                    definition_name = self.get_definition_name(referenced_model)

                properties[key] = {
                    u'type': u'array',
                    u'items': {
                        u'$ref': u'#/definitions/{}'.format(definition_name)
                    }
                }

        return {
            u'type': u'object',
            u'properties': properties
        }

    def create_list(self, model):
        definition_name = self.get_definition_name(model)

        return {
            u'type': u'array',
            u'items': {
                u'$ref': u'#/definitions/{}'.format(definition_name)
            }
        }

    def get_definition_name(self, model):
        # type: (object) -> unicode
        return self.integration.model_to_collection_names(model)[0].lower()

