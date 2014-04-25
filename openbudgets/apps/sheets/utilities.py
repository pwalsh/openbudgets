from django.conf import settings


def is_node_comparable(instance):

    """Sets the value of TemplateNode.comparable to True or False.

    Relies on the non-abstract TemplateNode implementation where nodes
    can belong to many templates.

    """

    value = settings.OPENBUDGETS_COMPARABLE_TEMPLATENODE

    if all([t.is_blueprint for t in instance.templates.all()]):
        value = settings.OPENBUDGETS_COMPARABLE_TEMPLATENODE_IN_BLUEPRINT
    else:
        value = settings.OPENBUDGETS_COMPARABLE_TEMPLATENODE_NOT_IN_BLUEPRINT

    return value
