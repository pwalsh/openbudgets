from openbudgets.apps.tools import factories
from openbudgets.commons import tests


class ToolAPITestCase(tests.OpenBudgetsAPITestCase):

    listview_name = 'tool-list'
    detailview_name = 'tool-detail'

    def setUp(self):
        self.object = factories.Tool.create()

    def test_listview(self):
        return ToolAPITestCase.listview(self)

    def test_detailview(self):
        return ToolAPITestCase.detailview(self)


class StateAPITestCase(tests.OpenBudgetsAPITestCase):

    listview_name = 'state-list'
    detailview_name = 'state-detail'

    def setUp(self):
        self.object = factories.State.create()

    def test_listview(self):
        return StateAPITestCase.listview(self)

    def test_detailview(self):
        return StateAPITestCase.detailview(self)
