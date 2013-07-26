"""Custom helpers for working with Django Forms"""

from django.template import Library


register = Library()


@register.inclusion_tag('partials/_form_field.html')
def field_generator(field, hidden=0, help=1, custom_label='', custom_class='',
                    inline_styles='', placeholder=''):
    """Returns a customized chunk of HTML for the given form field"""
    if custom_label:
        field.label = custom_label
    return {'field': field, 'hidden': hidden, 'help': help,
            'custom_class': custom_class, 'inline_styles': inline_styles}
