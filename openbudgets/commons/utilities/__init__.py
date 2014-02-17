"""Some helper functions for the project"""
import os


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


def get_media_file_path(instance, filename):
    """Puts any uploaded file in the right place."""
    tmp, ext = os.path.splitext(filename)
    value = os.path.join(
        instance.get_class_name(),
        unicode(instance.uuid) + ext)
    return value


def commas_format(value):
    if value is None:
        res = None
    else:
        res = '{:,}'.format(value)
        parts = res.split('.')
        if len(parts) > 1:
            res = parts[0]
    return res

