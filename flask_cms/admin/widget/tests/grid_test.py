from flask_cms.page.models import Page
from flask_cms.testing import TestCase
from flask_cms.widget.models.grid import Grid, GridPage
from flask_cms.widget.models.widget import Widget
from flask_cms.widget.models.widget_type import WidgetType


class AdminGridTest(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.admin_user = self._create_admin_user(
            email='admin@admin.com', password='password',
            active=True
        )
        self.user1 = self._create_user(
            email='fu@bar.com', password='password',
            active=True)
        self.widget_type = self._create_model(
            WidgetType,
            name="grid",
        )
        self.page1 = self._create_model(
            Page,
            title='fu1',
            description='bar1',
            slug='111',
        )
        self.page2 = self._create_model(
            Page,
            title='fu2',
            description='bar2',
            slug='222',
        )
        self.page3 = self._create_model(
            Page,
            title='fu3',
            description='bar3',
            slug='333',
        )

    def test_create_grid_as_admin(self):
        self.login_user(self.admin_user)
        self.app.post("/admin/widget",
                      data={
                          "name": "test_grid",
                          "types": self.widget_type.id,
                          "grid_types": "1_by_3_grid",
                          "grid_pages-0-page_slug": self.page1.slug,
                          "grid_pages-1-page_slug": self.page2.slug,
                          "grid_pages-2-page_slug": self.page3.slug,
                      })
        grid_widget = self._get_model(Widget, name="test_grid")
        assert grid_widget
        self.assertEquals(self.widget_type, grid_widget.widget_type)
        grid = self._get_model(Grid, widget_id=grid_widget.id)
        assert grid
        self.assertEquals("1_by_3_grid", grid.grid_type)
        assert self.page1 in grid.pages
        assert self.page2 in grid.pages
        assert self.page3 in grid.pages

    def test_create_grid_with_non_existing_pages_as_admin(self):
        self.login_user(self.admin_user)
        self.app.post("/admin/widget",
                      data={
                          "name": "test_grid",
                          "types": self.widget_type.id,
                          "grid_types": "1_by_3_grid",
                          "grid_pages-0-page_slug": "bpp",
                          "grid_pages-1-page_slug": "dsada",
                          "grid_pages-2-page_slug": "dsad",
                      })
        grid_widget = self._get_model(Widget, name="test_grid")
        assert grid_widget is None
        assert Grid.query.first() is None
        assert GridPage.query.first() is None
