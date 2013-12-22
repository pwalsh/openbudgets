from openbudgets.apps.contexts import factories
from openbudgets.commons import tests


class ContextAPITestCase(tests.OpenBudgetsAPITestCase):

    listview_name = 'context-list'
    detailview_name = 'context-detail'

    def setUp(self):
        self.object = factories.Context.create()

    def test_listview(self):
        return ContextAPITestCase.listview(self)

    def test_detailview(self):
        return ContextAPITestCase.detailview(self)


class CoefficientAPITestCase(tests.OpenBudgetsAPITestCase):

    listview_name = 'coefficient-list'
    detailview_name = 'coefficient-detail'

    def setUp(self):
        self.object = factories.Coefficient.create()

    def test_listview(self):
        return CoefficientAPITestCase.listview(self)

    def test_detailview(self):
        return CoefficientAPITestCase.detailview(self)
