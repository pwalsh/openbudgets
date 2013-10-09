from django.utils.translation import ugettext_lazy as _
#from django.core.urlresolvers import reverse
from grappelli.dashboard import modules, Dashboard


class OpenBudgetsDashboard(Dashboard):
    """Custom admin dashboard for Open Budget"""

    def init_with_context(self, context):

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('User management'),
            collapsible=True,
            column=1,
            css_classes=('collapse closed',),
            models=('openbudget.apps.accounts.*', 'oauth2_provider.*'),
        ))

        self.children.append(modules.AppList(
            _('Government entities'),
            collapsible=True,
            column=1,
            css_classes=('collapse closed',),
            models=('openbudget.apps.entities.*',),
        ))

        self.children.append(modules.AppList(
            _('Budget records'),
            collapsible=True,
            column=1,
            css_classes=('collapse closed',),
            models=('openbudget.apps.sheets.*',),
        ))

        self.children.append(modules.AppList(
            _('Budget taxonomies'),
            collapsible=True,
            column=1,
            css_classes=('collapse closed',),
            models=('openbudget.apps.taxonomies.*',),
        ))

        self.children.append(modules.AppList(
            _('Transport'),
            collapsible=True,
            column=1,
            css_classes=('collapse closed',),
            models=('openbudget.apps.transport.*',),
        ))

        self.children.append(modules.AppList(
            _('Generic pages'),
            collapsible=True,
            column=1,
            css_classes=('collapse closed',),
            models=('openbudget.apps.pages.*',),
        ))

        self.children.append(modules.AppList(
            _('Generic pages'),
            collapsible=True,
            column=1,
            css_classes=('collapse closed',),
            models=('openbudget.apps.tools.*',),
        ))

        self.children.append(modules.LinkList(
            _('File management'),
            column=2,
            children=[
                {
                    'title': _('Media browser'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                },
                {
                    'title': _('Codebase translations'),
                    'external': False,
                },
            ]
        ))

        self.children.append(modules.LinkList(
            _('External resources'),
            column=2,
            children=[
                {
                    'title': _('Open Budget Documentation'),
                    'url': 'http://open-budget.readthedocs.org/en/latest/',
                    'external': True,
                },
                {
                    'title': _('Django Documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Grappelli Documentation'),
                    'url': 'http://packages.python.org/django-grappelli/',
                    'external': True,
                },
                {
                    'title': _('Open Budget Repository'),
                    'url': 'https://github.com/prjts/open-budget',
                    'external': True,
                },
            ]
        ))

        self.children.append(modules.LinkList(
            _('Credits'),
            column=2,
            children=[
                {
                    'title': _('HaSadna'),
                    'url': 'http://hasadna.org.il/en/',
                    'external': True,
                },
                {
                    'title': _('Developed by prjts'),
                    'url': 'http://prjts.com/',
                    'external': True,
                },
                {
                    'title': _('Email developers'),
                    'url': 'mailto:hello@prjts.com',
                    'external': True,
                },
                {
                    'title': _('Designed by bnop'),
                    'url': 'http://bnop.co/',
                    'external': True,
                },
                {
                    'title': _('Email designers'),
                    'url': 'mailto:',
                    'external': True,
                },
            ]
        ))
        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))
