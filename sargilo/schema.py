from datetime import date, datetime, time
from typing import Dict, Type, List

from sargilo.collection import Collection
from sargilo.relations import (
    IncomingForeignKeyRelation,
    OutgoingForeignKeyRelation,
    ManyToManyRelation
)

TypeMapping = Dict[str, Type]


class JSONSchema:
    def __init__(self, type_mappings):
        # type: (Dict[Collection, TypeMapping]) -> JSONSchema
        self.type_mappings = type_mappings

        self.definitions = dict()
        self.top_level_properties = list()
        self.collections = type_mappings.keys()

    def generate(self):
        for collection_name, type_mapping in self.type_mappings.items():
            self.definitions[collection_name] = self.create_definition(type_mapping)

    def create_definition(self, type_mapping):
        # type: (TypeMapping) -> dict
        properties = dict()

        for key, expected_type in type_mapping.items():
            if expected_type is str:
                properties[key] = {
                    'type': 'string'
                }
            if expected_type is int:
                properties[key] = {
                    'type': 'integer'
                }

            if expected_type is date:
                # TODO: Add format validator
                properties[key] = {
                    'type': 'string'
                }

            if issubclass(expected_type, OutgoingForeignKeyRelation):
                referenced_definition = self.get_collection_name_by_model(expected_type.__args__[0])

                if not referenced_definition:
                    continue

                properties[key] = {
                    '$ref': '#/definitions/{}'.format(referenced_definition)
                }

            if issubclass(expected_type, IncomingForeignKeyRelation):
                referenced_definition = self.get_collection_name_by_model(expected_type.__args__[0])

                if not referenced_definition:
                    continue

                properties[key] = {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/{}".format(referenced_definition)
                    }
                }

            if issubclass(expected_type, ManyToManyRelation):
                referenced_definition = self.get_collection_name_by_model(expected_type.__args__[1])

                if not referenced_definition:
                    continue

                properties[key] = {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/{}".format(referenced_definition)
                    }
                }

        return {
            "type": "object",
            "properties": properties
        }

    def get_collection_name_by_model(self, model):
        # type: (object) -> Union[str, None]
        try:
           return next(c.name for c in self.collections if c.config.model is model)
        except StopIteration:
            return None

