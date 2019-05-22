from datetime import datetime, date, time
import sys

from ruamel import yaml
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from typing import Union, List, Dict
from django.db.models import Model

from .collection import Collection, CollectionConfig
from .integrations.base import Integration
from .relations import (
    IncomingForeignKeyRelation,
    OutgoingForeignKeyRelation,
    ManyToManyRelation
)


DATE_FORMAT = '%d.%m.%Y'
TIME_FORMAT = '%H:%M'
DATETIME_FORMAT = DATE_FORMAT + ' ' + TIME_FORMAT


# TODO: Find appropriate place for helper function
def get_anchor_value(map):
    # type: (CommentedMap) -> Union[str, None]
    try:
        return str(map.anchor.value)
    except AttributeError:
        return None


class ItemRegistry:
    """
    Stores all items and their corresponding anchor.
    """
    def __init__(self):
        self.registry = dict()  # type: Dict[str, object]

    def add_item(self, anchor, instance):
        # type: (str, object) -> None
        if anchor:
            self.registry[anchor] = instance

    def get_item(self, anchor):
        # type: (str) -> object
        try:
            return self.registry.get(anchor)
        except KeyError:
            return None


class Dataset:
    """
    The entirety of data used for testing.
    """

    # TODO: amend type hint for dataset_file to Path with Python3
    def __init__(self, dataset_file, config, integration):
        # type: (str, List[CollectionConfig], Integration) -> Dataset
        self.dataset_file = dataset_file
        self.config = config
        self.integration = integration

        self.data = None
        self.collections = list()  # type: List[Collection]
        self.items = ItemRegistry()

    def read_dataset(self):
        # type: () -> None
        """
        Reads in the dataset file, preserving the anchor information.
        """
        with open(self.dataset_file) as f:
            raw_data = f.read()

        try:
            self.data = yaml.round_trip_load(raw_data)
        except yaml.YAMLError:
            print('Something is not right with your yaml')
            sys.exit(1)

    # TODO: Remove as there are no longer sections
    def create_collections(self):
        # type: () -> None
        """
        Looks at read in data, extracts the configuration and creates
        `Collection` objects.
        """
        for collection_name in list(self.data.keys()):
            collection = Collection(
                name=collection_name,
                config=self.config[collection_name],
                data=self.data[collection_name],
            )

            self.collections += [collection]

    def create_objects(self):
        # type: () -> None
        for current_collection in self.collections:
            # Get information about collection

            if not current_collection.data:
                return

            for raw_item in current_collection.data:
                self.create_object(current_collection, raw_item)

    def get_object(self, value):
        # type: (object) -> Union[object, None]
        if hasattr(value, 'anchor') and value.anchor.value:
            return self.items.get_item(get_anchor_value(value))
        return None

    def process_string_value(self, value):
        try:
            return str(value)
        except UnicodeEncodeError as e:
            raise UnicodeEncodeError('Cannot decode the following value due to unicode issues: {}'
                                     'This might be caused by python2'.format(value))

    def process_integer_value(self, value):
        return int(value)

    def process_boolean_value(self, value):
        return bool(value)

    def process_date_value(self, value):
        return datetime.strptime(value, DATE_FORMAT).date()

    def process_time_value(self, value):
        """
        Checks if the given value can be converted to a `time` objects and
        does so if possible. Otherwise, an error is thrown.
        """
        return datetime.strptime(value, TIME_FORMAT).time()

    def process_datetime_value(self, value):
        return datetime.strptime(value, DATETIME_FORMAT)

    def process_outgoing_foreignkey_relationship(self, value, expected_type):
        """
        Processes an outgoing foreign key. This is a key that was declared at the model
        we are currently looking at and points to another model. There are three possible
        scenarios here:
        - the given value has an anchor set and no data, then try to grab the referenced item
        - the given value contains raw data, so the item should be created
        - the value is an already created instance (e.g. backlink of a through model); then just take this
        """
        if isinstance(value, Model):
            return value

        existing_object = self.get_object(value)
        if existing_object:
            return existing_object
        else:
            referenced_model = expected_type.__args__[0]
            referenced_collection = self.find_collection_by_model(referenced_model)

            if isinstance(value, CommentedSeq):
                raise ValueError('An outgoing foreign key relation can contain only one element, not a list')

            return self.create_object(
                collection=referenced_collection,
                raw_item=value
            )

    def process_incoming_foreignkey_relationship(self, value, expected_type, instance):
        """
        Processes an incoming foreign key, which was declared at another model and points
        to model currently in question. In the dataset file, the elements pointing to the created
        instance can be either full instances or anchors to an item.
        """
        referenced_model = expected_type.__args__[0]
        referenced_collection = self.find_collection_by_model(referenced_model)

        for child_data in value:
            self.create_object(
                collection=referenced_collection,
                raw_item=child_data,
                parent_instance=instance
            )

    def process_m2m_relationship(self, value, collection, expected_type, instance):
        # Describe relationship
        first_model = collection.config.model
        through_model, second_model = expected_type.__args__

        if through_model is not type(None):
            # M2M relation with intermediary model;
            # To process this relationship, we have to create instances of the intermediary model
            # with its constructor
            #
            # What to do:
            # - inspect intermediary model and find field that links it back to from_model
            # - put parent instance into this field
            # - create intermediary model instance
            through_collection = self.find_collection_by_model(through_model)
            type_mapping = self.integration.introspect_collection(through_collection.config)

            for a, t in type_mapping.items():
                if issubclass(t, OutgoingForeignKeyRelation) and t.__args__[0] == first_model:
                    backlink = a
                    break
            else:
                raise ValueError('Through model {} has no link back to {}'.format(through_model, first_model))

            for item_data in value:
                item_data[backlink] = instance
                self.create_object(
                    collection=through_collection,
                    raw_item=item_data
                )
        else:
            # M2M relation without intermediary model
            #
            # What to do:
            # - create instance
            # - find corresponding manager at parent instance
            # - add fresh instance to relation via manager
            collection_of_second_model = self.find_collection_by_model(second_model)

            for item_data in value:
                self.create_object(
                    collection=collection_of_second_model,
                    raw_item=item_data,
                    parent_instance=instance
                )

    def create_object(self, collection, raw_item, parent_instance=None):
        # type: (Collection, dict, object) -> object
        data = dict()
        anchor = get_anchor_value(raw_item)
        type_map = self.integration.introspect_collection(collection.config)

        basic_type_mapping = {
            str: self.process_string_value,
            int: self.process_integer_value,
            bool: self.process_boolean_value,
            date: self.process_date_value,
            time: self.process_time_value,
            datetime: self.process_datetime_value,
        }

        # Process values before creation of instance
        for key, value in raw_item.items():  # type: (str, Union[CommentedMap, object])
            expected_type = type_map[key]

            # Process basic types
            try:
                data[key] = basic_type_mapping[expected_type](value)
                continue
            except KeyError:
                pass

            # Process relations
            if issubclass(expected_type, OutgoingForeignKeyRelation):
                data[key] = self.process_outgoing_foreignkey_relationship(value, expected_type)

        # Create actual instance
        instance = self.integration.create_instance(config=collection.config, data=data, parent_instance=parent_instance)
        if anchor:
            self.items.add_item(anchor, instance)

        # Post-process m2m relations and incoming foreign key relations
        for key, value in raw_item.items():  # type: (str, Union[CommentedMap, object])
            expected_type = type_map[key]

            if issubclass(expected_type, IncomingForeignKeyRelation):
                self.process_incoming_foreignkey_relationship(value, expected_type, instance)

            if issubclass(expected_type, ManyToManyRelation):
                self.process_m2m_relationship(
                    value=value,
                    expected_type=expected_type,
                    collection=collection,
                    instance=instance
                )

        return instance

    def find_collection_by_model(self, model):
        # type: (object) -> Collection
        for collection in self.collections:
            if collection.config.model is model:
                return collection
        else:
            raise ValueError('No collection for model {} found'.format(model))
