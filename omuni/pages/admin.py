from django.contrib import admin
from omuni.pages.models import Page
from modeltranslation.admin import TranslationAdmin


class PageAdmin(TranslationAdmin):

    class Media:

        js = (

            # for modeltranslation
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
            # for grappelli
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/js/tinymce.js',
        )

        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


admin.site.register(Page, PageAdmin)
