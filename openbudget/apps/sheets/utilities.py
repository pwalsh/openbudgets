from django.conf import settings


def is_comparable():

    """Sets the value of TemplateNode.comparable to True or False."""

    value = settings.OPENBUDGETS_COMPARABLE_TEMPLATENODE__DEFAULT
    return value
