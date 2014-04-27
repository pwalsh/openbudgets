from django.conf import settings


def is_node_comparable(instance):

    """Sets the value of TemplateNode.comparable to True or False.

    Relies on the non-abstract TemplateNode implementation where nodes
    can belong to many templates.

    """

    if settings.OPENBUDGETS_COMPARABLE_STRICT_BY_DECLARATION:
        return instance.comparable

    value = settings.OPENBUDGETS_COMPARABLE_NODE_DEFAULT

    if any([t.is_blueprint for t in instance.templates.all()]):
        # if the node is a blueprint node, take that setting
        value = settings.OPENBUDGETS_COMPARABLE_NODE_IN_BLUEPRINT
    else:
        # if the node is not a blueprint node, take that setting
        value = settings.OPENBUDGETS_COMPARABLE_NODE_NOT_IN_BLUEPRINT

    if settings.OPENBUDGETS_COMPARABLE_OVERRIDE_BY_INHERITANCE:
        # override by inheritance means that we take the value of the parent
        # and (potentially) override the basic configuration above.
        value = instance.parent.comparable

    return value
