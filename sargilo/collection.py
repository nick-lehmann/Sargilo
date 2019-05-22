from typing import Dict
from .item import Item

# RELATION_FIELDS = (
#     models.ForeignKey,
#     models.OneToOneField,
#     models.ManyToManyField
# )


class CollectionConfig:
    """
    Stores information about how to create a concrete object
    based on what is stored in the collection.
    """

    def __init__(self, model=None, creation_function=None):
        self.model = model
        self.creation_function = creation_function


class Collection:
    """
    Container for several items.
    """

    def __init__(self, name, config, data):
        # type: (str, CollectionConfig, dict) -> Collection
        self.name = name
        self.config = config
        self.data = data
        self.items = list()

    def __str__(self):
        # type: () -> str
        return 'Collection {} for model {} with {} items'.format(
            self.name,
            self.config.model,
            len(self.data)
        )

    # def create_objects(self):
    #     for item in self.data:
    #         print('Start to create the following object: {}'.format(item))
    #
    #         creation_kwargs = dict()
    #
    #         for item_field_name, item_field_value in item.items():
    #             model_field = self.item_field_to_model_field(item_field_name)
    #             if type(model_field) in RELATION_FIELDS:
    #                 # YAML allows referencing another object by its anchor.
    #                 # The pointer to that object is called an alias.
    #                 alias = item_field_value.anchor.value
    #                 referenced_item = self.find_object_by_anchor(alias)
    #                 referenced_object = referenced_item.object
    #
    #                 creation_kwargs[item_field_name + '_id'] = referenced_object.id
    #             else:
    #                 creation_kwargs[item_field_name] = item_field_value
    #
    #         # if self.model is User:
    #         #     object = User.objects.create_user(**creation_kwargs)
    #         # else:
    #         #     object = self.model(**creation_kwargs)
    #         #     object.save()
    #         object = self.model(**creation_kwargs)
    #         object.save()
    #         print('Created {}'.format(object))
    #
    #         new_item = Item(anchor=item.anchor.value, object=object)
    #         self.items.append(new_item)

    # def item_field_to_model_field(self, field_name):
    #     """
    #     Given the name of a collection field, this function will return
    #     the corresponding model field by looking up the name.
    #     """
    #     for model_field in self.model._meta.fields:
    #         if model_field.name == field_name:
    #             return model_field



    def find_object_by_anchor(self, anchor):
        # type: (str) -> object
        return self.dataset.find_object_by_anchor(anchor)
