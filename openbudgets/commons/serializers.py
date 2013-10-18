from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField


class UUIDRelatedField(SlugRelatedField):
    """
    Represents a relationship using a UUID field on the target.
    """

    def __init__(self, *args, **kwargs):
        self.slug_field = 'uuid'
        super(SlugRelatedField, self).__init__(*args, **kwargs)

    def to_native(self, value):
        return str(value.uuid)


class UUIDPKRelatedField(PrimaryKeyRelatedField):
    """
    Represents a relationship using a UUID field on the target.
    """

    def to_native(self, pk):
        return str(pk)
