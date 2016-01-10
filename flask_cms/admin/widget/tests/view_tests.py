from flask_cms.ext import db
from flask_cms.page.models import Page, PageWidget
from flask_cms.testing import TestCase
from flask_cms.widget.models.poll import Poll, Choice
from flask_cms.widget.models.widget import Widget
from flask_cms.widget.models.widget_type import WidgetType


class AdminWidgetTest(TestCase):
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
            name="poll",
        )
        self.widget = self._create_model(
            Widget,
            name="test_widget",
            widget_type_id=self.widget_type.id,
        )


class CreateWidgetViewTest(AdminWidgetTest):
    def test_get_widget_form_as_admin(self):
        self.login_user(self.admin_user)
        response = self.app.get("/admin/widget")
        self.assertEquals(200, response.status_code)

    def test_get_widget_form_as_non_admin(self):
        self.login_user(self.user1)
        response = self.app.get("/admin/widget")
        self.assertEquals(302, response.status_code)

    def test_get_widget_form_as_anonymous(self):
        response = self.app.get("/admin/widget")
        self.assertEquals(302, response.status_code)

    def test_create_widget_as_admin(self):
        self.login_user(self.admin_user)
        self.app.post("/admin/widget",
                      data={
                          "name": "fu_widget",
                          "types": self.widget_type.id,
                          "question": "fu",
                          "choice1": "bar",
                          "choice2": "car",
                      })

        widget = self._get_model(Widget, name="fu_widget")
        assert widget
        self.assertEquals("fu", widget.poll.question)
        choices = [c.description for c in widget.poll.choices]
        assert "bar" in choices
        assert "car" in choices
        self.assertEquals(0, widget.poll.choices[0].vote)
        self.assertEquals(0, widget.poll.choices[1].vote)

    def test_create_widget_as_non_admin(self):
        self.login_user(self.user1)
        response = self.app.post("/admin/widget",
                                 data={
                                     "name": "test_widget",
                                     "types": self.widget_type.id,
                                     "question": "fu",
                                     "choice1": "bar",
                                     "choice2": "car",
                                 })
        self.assertEquals(302, response.status_code)

    def test_create_widget_as_anonymous(self):
        response = self.app.post("/admin/widget",
                                 data={
                                     "name": "test_widget",
                                     "types": self.widget_type.id,
                                     "question": "fu",
                                     "choice1": "bar",
                                     "choice2": "car",
                                 })
        self.assertEquals(302, response.status_code)


class ShowWidgetViewTest(AdminWidgetTest):
    def test_show_widget_with_component(self):
        poll = Poll(question="fu")
        poll.widget = self.widget
        choice = Choice(description="bar")
        poll.choices.append(choice)
        db.session.add(poll)
        db.session.commit()

        self.login_user(self.admin_user)
        response = self.app.get("/admin/widget/{}".format(self.widget.id))
        self.assertEquals(200, response.status_code)

    def test_show_widget_without_component(self):
        self.login_user(self.admin_user)
        response = self.app.get("/admin/widget/{}".format(self.widget.id))
        self.assertEquals(302, response.status_code)

    def test_show_widget_as_non_admin(self):
        self.login_user(self.user1)
        response = self.app.get("/admin/widget/{}".format(self.widget.id))
        self.assertEquals(302, response.status_code)

    def test_show_widget_as_anonymous(self):
        response = self.app.get("/admin/widget/{}".format(self.widget.id))
        self.assertEquals(302, response.status_code)


class DeleteWidgetViewTest(AdminWidgetTest):
    def test_delete_widget_with_component(self):
        poll = Poll(question="fu")
        poll.widget = self.widget
        choice = Choice(description="bar")
        poll.choices.append(choice)
        db.session.add(poll)
        db.session.commit()

        self.login_user(self.admin_user)
        self.app.get("/admin/widget/{}/delete".format(self.widget.id))
        widget = self._get_model(Widget, name="test_widget")
        poll = self._get_model(Poll, question="fu")
        choice = self._get_model(Choice, description="bar")
        assert widget is None
        assert poll is None
        assert choice is None

    def test_delete_widget_added_to_page_should_remove_association_with_page(self):
        page = self._create_model(
            Page,
            slug='fu', title='parent',
            description='description',
            level=0, widgets=[self.widget]
        )

        assert self.widget in page.widgets

        self.login_user(self.admin_user)
        self.app.get("/admin/widget/{}/delete".format(self.widget.id))

        assert self._get_page(slug='fu') is not None
        assert self._get_model(Widget, id=self.widget.id) is None
        assert self._get_model(PageWidget, widget_id=self.widget.id) is None

    def test_delete_widget_as_non_admin(self):
        self.login_user(self.user1)
        response = self.app.get("/admin/widget/{}/delete".format(self.widget.id))
        self.assertEquals(302, response.status_code)

    def test_delete_widget_as_anonymous(self):
        response = self.app.get("/admin/widget/{}/delete".format(self.widget.id))
        self.assertEquals(302, response.status_code)


class WidgetIndexViewTest(AdminWidgetTest):
    def test_list_widget_as_admin(self):
        self.login_user(self.admin_user)
        response = self.app.get('/admin/widget/list')
        self.assertEquals(200, response.status_code)

    def test_list_widget_as_non_admin(self):
        self.login_user(self.user1)
        response = self.app.get('/admin/widget/list')
        self.assertEquals(302, response.status_code)

    def test_list_widget_anonymous(self):
        response = self.app.get('/admin/widget/list')
        self.assertEquals(302, response.status_code)


class CreateWidgetTypeTest(AdminWidgetTest):
    def test_create_widget_type_as_admin(self):
        self.login_user(self.admin_user)
        self.app.post("/admin/widget_type",
                      data={'name': 'fubar'})
        widget_type = self._get_model(WidgetType,
                                      name='fubar')
        assert widget_type

    def test_create_widget_type_as_non_admin(self):
        self.login_user(self.user1)
        self.app.post("/admin/widget_type",
                      data={'name': 'fubar'})
        widget_type = self._get_model(WidgetType,
                                      name='fubar')
        assert widget_type is None

    def test_create_widget_type_as_anonymous(self):
        self.app.post("/admin/widget_type",
                      data={'name': 'fubar'})
        widget_type = self._get_model(WidgetType,
                                      name='fubar')
        assert widget_type is None


class DeleteWidgetTypeTest(AdminWidgetTest):
    def test_delete_widget_type_as_admin(self):
        self.login_user(self.admin_user)
        self._create_model(WidgetType, name='fubar')
        widget_type = self._get_model(WidgetType,
                                      name='fubar')
        assert widget_type

        self.app.get("/admin/widget_type/delete/{}".format(widget_type.id))
        widget_type = self._get_model(WidgetType,
                                      id=widget_type.id)
        assert widget_type is None

    def test_delete_widget_type_as_non_admin(self):
        self.login_user(self.user1)
        self._create_model(WidgetType, name='fubar')
        widget_type = self._get_model(WidgetType,
                                      name='fubar')
        assert widget_type

        self.app.get("/admin/widget_type/delete/{}".format(widget_type.id))
        widget_type = self._get_model(WidgetType,
                                      id=widget_type.id)
        assert widget_type

    def test_delete_widget_type_as_anonymous(self):
        self._create_model(WidgetType, name='fubar')
        widget_type = self._get_model(WidgetType,
                                      name='fubar')
        assert widget_type

        self.app.get("/admin/widget_type/delete/{}".format(widget_type.id))
        widget_type = self._get_model(WidgetType,
                                      id=widget_type.id)
        assert widget_type
