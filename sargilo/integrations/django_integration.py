from datetime import datetime, date

from .base import Integration
from sargilo.collection import CollectionConfig
from sargilo.relations import (
    IncomingForeignKeyRelation,
    OutgoingForeignKeyRelation,
    ManyToManyRelation
)

from django.db.models import Model as DjangoModel
from django.db.models import get_model, get_models
from django.db.models.fields import (
    Field,
    AutoField,                  # should be ignored
    CharField, TextField, EmailField,
    IntegerField,
    BooleanField,
    DateField
)
from django.db.models.fields.related import (
    ForeignKey, ForeignRelatedObjectsDescriptor,
    ManyToManyField
)

IGNORED_FIELDS = [AutoField]
DJANGO_FIELD_TO_TYPE_MAPPING = {
    CharField: str,
    TextField: str,
    EmailField: str,
    DateField: date,
    BooleanField: bool,
    IntegerField: int,
}


class DjangoIntegration(Integration):
    """
    This class fills the gap between Django and Sargilo by providing the following features:
    - determines dependency of a model
    """

    def create_instance(self, config, data, parent_instance=None):
        # type: (CollectionConfig, dict, object) -> object
        """
        Creates an instance of the Django model specified in the CollectionConfig with
        the prepared data.
        """
        model = config.model

        if not parent_instance:
            concrete_creation_function = config.creation_function(model)
            model_instance = concrete_creation_function(**data)
        else:
            child_model = config.model

            for attribute_name in dir(parent_instance):
                if attribute_name in ['objects', 'base_objects']:
                    continue

                attribute = getattr(parent_instance, attribute_name)

                if type(attribute).__name__ in ['RelatedManager', 'ManyRelatedManager'] and attribute.model is child_model:
                    return attribute.create(**data)
            else:
                raise ValueError('Parent {} and child {} do not seem to be related'.format(parent_instance, child_model))

        return model_instance

    def introspect_collection(self, collection_config=None, model=None):
        # type: (CollectionConfig, DjangoModel) -> dict
        assert collection_config or model

        if not model:
            model = collection_config.model  # type: DjangoModel

        field_to_type_mapping = dict()

        # Add "normal" fields and outgoing foreign key relations
        for field in model._meta.fields:  # type: Field
            if field in IGNORED_FIELDS:
                continue

            field_name = field.name

            for field_type, python_type in DJANGO_FIELD_TO_TYPE_MAPPING.items():
                if issubclass(type(field), field_type):
                    field_to_type_mapping[field_name] = python_type

            if type(field) in DJANGO_FIELD_TO_TYPE_MAPPING:
                field_type = DJANGO_FIELD_TO_TYPE_MAPPING.get(type(field))
                field_to_type_mapping[field_name] = field_type

            if type(field) is ForeignKey:
                referenced_model = field.rel.to
                field_to_type_mapping[field_name] = OutgoingForeignKeyRelation[referenced_model]

        # Add incoming foreign key relations
        for attribute_name in dir(model):  # type: str
            attribute = getattr(model, attribute_name)
            if type(attribute) == ForeignRelatedObjectsDescriptor and not attribute_name.endswith('_set'):
                referencing_model = attribute.related.model
                field_to_type_mapping[attribute_name] = IncomingForeignKeyRelation[referencing_model]

        # Add many-to-many relations
        for m2m_field in model._meta.many_to_many:  # type: ManyToManyField
            relation_name = m2m_field.attname
            referenced_model = m2m_field.rel.to    # type: DjangoModel
            through_model = m2m_field.rel.through  # type: DjangoModel

            # Do not use auto-created intermediary models
            if through_model._meta.auto_created:
                through_model = None

            field_to_type_mapping[relation_name] = ManyToManyRelation[through_model, referenced_model]

        return field_to_type_mapping

    def model_to_collection_names(self, model):
        # type: (Model) -> List[str]
        return [model._meta.object_name, '.'.join((model._meta.app_label, model._meta.object_name))]

    def collection_name_to_model(self, collection_name):
        # type: (str) -> Model
        if '.' in collection_name:
            app_label, model_name = collection_name.split('.')
            return get_model(app_label=app_label, model_name=model_name)
        else:
            return next(model for model in get_models() if model._meta.object_name == collection_name)
