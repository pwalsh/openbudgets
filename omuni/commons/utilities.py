"""Some helper scripts for the project"""


def get_ultimate_parent(obj):
    """Give me an object that has a parent attribute"""

    if obj.parent:
        get_ultimate_parent(obj.parent)
    else:
        return obj
