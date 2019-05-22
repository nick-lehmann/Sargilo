class Item:
    """
    Represents a single test data entry.
    - Anchor
    - Object (Database) and its id
    """
    def __init__(self, anchor, object):
        self.anchor = anchor
        self.object = object

    @property
    def id(self):
        return self.object.id