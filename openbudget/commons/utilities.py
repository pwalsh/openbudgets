"""Some helper functions for the project"""


def get_ultimate_parent(obj):
    """Returns the ultimate parent of any object.

    In order to get to the ultimate parent, we need to know
    how to find it. The default has is that the object has
    a property called parent.

    """
    if obj.parent:
        return get_ultimate_parent(obj.parent)
    else:
        return obj
