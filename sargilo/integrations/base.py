from typing import List, Optional
from django.db.models import Model, get_model, get_models
from ..collection import CollectionConfig


class Integration:
    def create_instance(self, config, data, parent_instance=None):
        # type: (CollectionConfig, dict, Optional[object]) -> object
        raise NotImplemented

    def introspect_collection(self, collection_config, model):
        # type: (CollectionConfig, object) -> dict
        raise NotImplemented

    def model_to_collection_names(self, model):
        # type: (Model) -> List[str]
        raise NotImplemented

    def collection_name_to_model(self, collection_name):
        # type: (str) -> Model
        raise NotImplemented
