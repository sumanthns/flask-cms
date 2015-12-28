from flask_cms.page.context_processors import get_breadcrumbs
from flask_cms.testing import TestCase


class PageViewTest(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.page = self._create_page(
            slug='page', title='title',
            description='description'
        )
        self.page_1 = self._create_page(
            slug='page1', title='title',
            description='description',
            login_required=True,
            parent_id=self.page.id
        )
        self.page_2 = self._create_page(
            slug='page2', title='title',
            description='description',
            login_required=True,
            parent_id=self.page_1.id
        )

    def test_breadcrumbs_are_in_top_down_order(self):
        breadcrumbs = get_breadcrumbs(self.page_2)
        self.assertEquals(['page', 'page1', 'page2'],
                          breadcrumbs)
