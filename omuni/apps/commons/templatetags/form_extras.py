"""Custom helpers for working with Django Forms"""

from django.template import Library

register = Library()

@register.inclusion_tag('partials/_form_field.html')
def field_generator(field, custom_label='', custom_class=''):
    """Returns a customized chunk of HTML for the given form field"""

    if custom_label:
        field.label = custom_label
    return {'field': field, 'custom_class': custom_class}
