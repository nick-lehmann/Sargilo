from ..collection import CollectionConfig
from typing import Optional


class Integration:
    def create_instance(self, config, data, parent_instance=None):
        # type: (CollectionConfig, dict, Optional[object]) -> object
        raise NotImplemented

    def introspect_collection(self, collection_config):
        # type: (CollectionConfig) -> dict
        raise NotImplemented
