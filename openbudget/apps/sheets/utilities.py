from django.conf import settings


def is_comparable():

    """Sets the value of TemplateNode.comparable to True or False."""

    value = settings.OPENBUDGETS_TEMPLATENODE_COMPARABLE_DEFAULT
    return value
