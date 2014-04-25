from rest_framework import relations


class UUIDRelatedField(relations.SlugRelatedField):

    """Returns a string representation of a UUID instance, where the relation is on a `uuid` field.

    This is required do to the way the UUIDField we depend on implements
    its to_python method.

    """

    def __init__(self, *args, **kwargs):
        super(UUIDRelatedField, self).__init__(*args, slug_field='uuid', **kwargs)

    def to_native(self, obj):
        return str(getattr(obj, self.slug_field))


class UUIDPrimaryKeyRelatedField(relations.PrimaryKeyRelatedField):

    """Returns a string representation of a UUID instance, where the `pk` is a UUID.

    This is required do to the way the UUIDField we depend on implements
    its to_python method.

    """

    def to_native(self, pk):
        if not pk:
            return None
        return str(pk)
