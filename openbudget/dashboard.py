from django.utils.translation import ugettext_lazy as _
#from django.core.urlresolvers import reverse
from grappelli.dashboard import modules, Dashboard


class OpenBudgetDashboard(Dashboard):
    """Custom admin dashboard for Open Budget"""

    def init_with_context(self, context):

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('User management'),
            collapsible=True,
            column=1,
            css_classes=('collapse closed',),
            models=('openbudget.apps.accounts.*',),
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
            models=('openbudget.apps.budgets.*',),
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

        self.children.append(modules.LinkList(
            _('Media management'),
            column=2,
            children=[
                {
                    'title': _('FileBrowser'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                },
                {
                    'title': _('Static translations'),
                    'url': '/rosetta/',
                    'external': False,
                },
            ]
        ))

        self.children.append(modules.LinkList(
            _('Support'),
            column=2,
            children=[
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
                    'title': _('Built by prjts'),
                    'url': 'http://prjts.com/',
                    'external': True,
                },
                {
                    'title': _('Email Paul Walsh (developer)'),
                    'url': 'mailto:paulywalsh@gmail.com',
                    'external': True,
                },
                {
                    'title': _('Email Yehonatan Daniv (developer)'),
                    'url': 'mailto:maggotfish@gmail.com',
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
