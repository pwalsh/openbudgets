"""Custom helpers for working with Django Forms"""

from django.template import Library

register = Library()

@register.inclusion_tag('partials/_form_field.html')
def field_generator(field, hidden=0, custom_label='', custom_class='', inline_styles=''):
    """Returns a customized chunk of HTML for the given form field"""
    print hidden
    if custom_label:
        field.label = custom_label
    return {'field': field, 'hidden': hidden, 'custom_class': custom_class, 'inline_styles': inline_styles}
