from typing import Generic, TypeVar


RelatedCollection = TypeVar('RelatedCollection')
ThroughCollection = TypeVar('ThroughCollection')


class OutgoingForeignKeyRelation(Generic[RelatedCollection]):
    @property
    def target_model(self):
        return self.__args__[0]


class IncomingForeignKeyRelation(Generic[RelatedCollection]):
    @property
    def target_model(self):
        return self.__args__[0]


class ManyToManyRelation(Generic[ThroughCollection, RelatedCollection]):
    def has_through_model(self):
        return self.through_model is not type(None)

    @property
    def through_model(self):
        return self.__args__[0]

    @property
    def target_model(self):
        return self.__args__[1]
