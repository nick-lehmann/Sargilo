from datetime import date, datetime, time
from typing import Dict, Type, Union

from sargilo.collection import Collection
from sargilo.relations import (
    IncomingForeignKeyRelation,
    OutgoingForeignKeyRelation,
    ManyToManyRelation
)

TypeMapping = Dict[str, Type]


class JSONSchema:
    # TODO: Implement requirements for each collection
    # TODO: Add validators to schema (e.g. minimum number for integers)
    def __init__(self, type_mappings):
        # type: (Dict[Collection, TypeMapping]) -> JSONSchema
        self.type_mappings = type_mappings

        self.definitions = dict()
        self.top_level_properties = dict()
        self.collections = type_mappings.keys()

    def generate(self):
        for collection, type_mapping in self.type_mappings.items():
            self.definitions[self.get_definition_name(collection.name)] = self.create_definition(type_mapping)
            self.top_level_properties[u'{}'.format(collection.name)] = self.create_list(collection)

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
                referenced_definition = self.get_collection_name_by_model(expected_type.__args__[0])

                if not referenced_definition:
                    continue

                definition_name = self.get_definition_name(referenced_definition)

                properties[key] = {
                    u'$ref': u'#/definitions/{}'.format(definition_name)
                }

            if issubclass(expected_type, IncomingForeignKeyRelation):
                referenced_definition = self.get_collection_name_by_model(expected_type.__args__[0])
                definition_name = self.get_definition_name(referenced_definition)

                if not referenced_definition:
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
                    referenced_definition = self.get_collection_name_by_model(through_model)
                else:
                    referenced_definition = self.get_collection_name_by_model(referenced_model)

                if not referenced_definition:
                    continue

                definition_name = self.get_definition_name(referenced_definition)

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

    def create_list(self, collection):
        model = collection.config.model
        definition_name = self.get_definition_name(self.get_collection_name_by_model(model))

        return {
            u'type': u'array',
            u'items': {
                u'$ref': u'#/definitions/{}'.format(definition_name)
            }
        }

    def get_definition_name(self, name):
        # type: (str) -> unicode
        if name.endswith('s'):
            name = name.rstrip('s')

        return u'{}'.format(name.lower())

    def get_collection_name_by_model(self, model):
        # type: (object) -> Union[unicode, None]
        try:
            return u'{}'.format(next(c.name for c in self.collections if c.config.model is model))
        except StopIteration:
            return None
