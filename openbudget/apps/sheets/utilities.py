from django.conf import settings


def is_comparable(instance):

    """Sets the value of TemplateNode.comparable to True or False."""

    value = True
    if instance.is_blueprint:
        value = settings.OPENBUDGETS_TEMPLATENODE_COMPARABLE_DEFAULT
    elif not instance.is_blueprint:
        value = settings.OPENBUDGETS_TEMPLATENODE_NOT_IN_BLUEPRINT_COMPARABLE_DEFAULT
    return value
