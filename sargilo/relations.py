from typing import Generic, TypeVar


RelatedCollection = TypeVar('RelatedCollection')
ThroughCollection = TypeVar('ThroughCollection')


class OutgoingForeignKeyRelation(Generic[RelatedCollection]):
    pass


class IncomingForeignKeyRelation(Generic[RelatedCollection]):
    pass


class ManyToManyRelation(Generic[ThroughCollection, RelatedCollection]):
    pass
