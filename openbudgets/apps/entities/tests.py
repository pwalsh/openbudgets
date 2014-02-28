from openbudgets.apps.entities import factories
from openbudgets.apps.contexts.factories import Context
from openbudgets.apps.sheets.factories import Sheet
from openbudgets.commons import tests


class EntityUITestCase(tests.OpenBudgetsUITestCase):

    listview_name = 'entity_list'
    detailview_name = 'entity_detail'

    def setUp(self):
        self.object = factories.Entity.create()
        self.entity_context = Context.create(entity=self.object)
        self.entity_sheet = Sheet.create(entity=self.object)

    def test_listview(self):
        return EntityUITestCase.listview(self)

    def test_detailview(self):
        return EntityUITestCase.detailview(self, lookup=self.object.slug)


class EntityAPITestCase(tests.OpenBudgetsAPITestCase):

    listview_name = 'entity-list'
    detailview_name = 'entity-detail'

    def setUp(self):
        self.object = factories.Entity.create()

    def test_listview(self):
        return EntityAPITestCase.listview(self)

    def test_detailview(self):
        return EntityAPITestCase.detailview(self)


class DivisionAPITestCase(tests.OpenBudgetsAPITestCase):

    listview_name = 'division-list'
    detailview_name = 'division-detail'

    def setUp(self):
        self.object = factories.Division.create()

    def test_listview(self):
        return DivisionAPITestCase.listview(self)

    def test_detailview(self):
        return DivisionAPITestCase.detailview(self)


class DomainAPITestCase(tests.OpenBudgetsAPITestCase):

    listview_name = 'domain-list'
    detailview_name = 'domain-detail'

    def setUp(self):
        self.object = factories.Domain.create()

    def test_listview(self):
        return DomainAPITestCase.listview(self)

    def test_detailview(self):
        return DomainAPITestCase.detailview(self)
