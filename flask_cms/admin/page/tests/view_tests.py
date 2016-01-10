from flask_cms.ext import db
from flask_cms.page.models import Page, PageWidget
from flask_cms.testing import TestCase
from flask_cms.widget.models.widget import Widget
from flask_cms.widget.models.widget_type import WidgetType


class AdminPageTest(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.admin_user = self._create_admin_user(
            email='admin@admin.com', password='password',
            active=True
        )
        self.user1 = self._create_user(
            email='fu@bar.com', password='password',
            active=True)
        self.template = self._create_template(
            name="blog_template",
            description="desc",
        )
        self.page = self._create_page(
            slug='test', title='title',
            description='description',
            template_id=self.template.id
        )


class EditPageViewTest(AdminPageTest):
    def test_get_as_admin(self):
        self.login_user(self.admin_user)
        response = self.app.get("/admin/page/test")

        self.assertEquals(response.status_code, 200)

    def test_get_as_non_admin(self):
        self.login_user(self.user1)
        response = self.app.get("/admin/page/test")

        self.assertEquals(response.status_code, 302)

    def test_get_as_anonymous(self):
        response = self.app.get("/admin/page/test")

        self.assertEquals(response.status_code, 302)

    def test_post_as_admin(self):
        template = self._create_template(
            name='fu_template',
            description='barred',
        )
        self.login_user(self.admin_user)
        self.app.post("/admin/page/test",
                      data={
                          'slug': 'fu',
                          'title': 'bar',
                          'templates': template.id,
                      })
        page = self._get_page(slug='fu')
        assert page
        self.assertFalse(page.login_required)
        self.assertEquals('bar', page.title)
        self.assertEquals(template, page.template)

    def test_post_as_non_admin(self):
        self.login_user(self.user1)
        response = self.app.post("/admin/page/test",
                                 data={
                                     'slug': 'fu',
                                     'title': 'bar',
                                 })
        self.assertEquals(response.status_code, 302)

    def test_post_as_anonymous(self):
        response = self.app.post("/admin/page/test",
                                 data={
                                     'slug': 'fu',
                                     'title': 'bar',
                                 })
        self.assertEquals(response.status_code, 302)


class DeletePageViewTest(AdminPageTest):
    def test_delete_as_admin(self):
        self._create_page(
            slug='fu', title='parent',
            description='description',
            level=0,
        )
        assert self._get_page(slug="fu")
        self.login_user(self.admin_user)
        self.app.get("/admin/page/fu/delete")
        assert self._get_page(slug='fu') is None

    def test_delete_with_children(self):
        parent = self._create_page(
            slug='fu', title='parent',
            description='description',
            level=0,
        )
        self._create_page(
            slug='bar', title='child',
            description='description',
            level=0, parent_id=parent.id
        )
        assert self._get_page(slug="fu")
        assert self._get_page(slug="bar")
        self.login_user(self.admin_user)
        self.app.get("/admin/page/fu/delete")
        assert self._get_page(slug='fu') is None
        assert self._get_page(slug='bar') is None

    def test_delete_with_widgets(self):
        page = self._create_model(
            Page,
            slug='fu', title='parent',
            description='description',
            level=0,
        )
        widget_type = self._create_model(
            WidgetType, name='test')
        widget = self._create_model(
            Widget, name='test_widget',
            widget_type_id=widget_type.id)
        page.widgets.append(widget)
        db.session.commit()

        page = self._get_page(slug='fu')
        assert widget in page.widgets

        self.login_user(self.admin_user)
        self.app.get("/admin/page/fu/delete")

        assert self._get_page(slug='fu') is None
        assert self._get_model(Widget, name='test_widget') is not None
        assert self._get_model(PageWidget, page_id=page.id) is None

    def test_delete_non_existing_page_404(self):
        self.login_user(self.admin_user)
        response = self.app.get("/admin/page/fu/delete")
        self.assertEquals(response.status_code, 404)

    def test_delete_as_non_admin(self):
        self.login_user(self.user1)
        response = self.app.get("/admin/page/fu/delete")
        self.assertEquals(response.status_code, 302)

    def test_delete_as_anonymous(self):
        response = self.app.get("/admin/page/fu/delete")
        self.assertEquals(response.status_code, 302)


class AddPageViewTest(AdminPageTest):
    def test_post_as_admin(self):
        self.login_user(self.admin_user)
        self.app.post("/admin/page",
                      data={
                          'slug': 'fu',
                          'title': 'bar',
                          'description': 'desc',
                          'login_required': True,
                          'templates': self.template.id,
                      })
        page = self._get_page(slug='fu')
        assert page
        assert page.login_required
        assert page.created_at is not None
        self.assertEquals(0, page.level)
        self.assertEquals('bar', page.title)
        self.assertEquals('desc', page.description)
        self.assertEquals(self.template, page.template)

    def test_post_as_admin_with_parent(self):
        self.parent = self._create_page(
            slug='parent', title='parent',
            description='description',
            level=0, template_id=self.template.id
        )
        self.login_user(self.admin_user)
        self.app.post("/admin/page",
                      data={
                          'slug': 'fu',
                          'title': 'bar',
                          'description': 'desc',
                          'login_required': True,
                          'parent_slug': 'parent',
                          'templates': self.template.id,
                      })
        page = self._get_page(slug='fu')
        assert page
        assert page.login_required
        self.assertEquals(1, page.level)
        self.assertEquals('bar', page.title)
        self.assertEquals('desc', page.description)
        self.assertEquals(page.parent, self.parent)

    def test_post_as_admin_missing_required_fields(self):
        self.login_user(self.admin_user)
        self.app.post("/admin/page",
                      data={
                          'slug': 'fu',
                          'title': 'bar',
                          'description': 'desc',
                          'login_required': True,
                      })
        page = self._get_page(slug='fu')
        assert page is None

    def test_post_as_non_admin(self):
        self.login_user(self.user1)
        response = self.app.post("/admin/page",
                                 data={
                                     'slug': 'fu',
                                     'title': 'bar',
                                 })
        self.assertEquals(response.status_code, 302)

    def test_post_as_anonymous(self):
        response = self.app.post("/admin/page",
                                 data={
                                     'slug': 'fu',
                                     'title': 'bar',
                                 })
        self.assertEquals(response.status_code, 302)


class AdminIndexViewTest(AdminPageTest):
    def test_get_as_admin(self):
        self.login_user(self.admin_user)
        response = self.app.get("/admin")
        self.assertEquals(200, response.status_code)

    def test_get_as_non_admin(self):
        self.login_user(self.user1)
        response = self.app.get("/admin")
        self.assertEquals(302, response.status_code)

    def test_get_as_anonymous(self):
        response = self.app.get("/admin")
        self.assertEquals(302, response.status_code)


class AddWidgetToPageViewTest(AdminPageTest):
    def setUp(self):
        AdminPageTest.setUp(self)
        self.widget_type = self._create_model(
            WidgetType, name='poll')
        self.widget = self._create_model(
            Widget, name='test_widget',
            widget_type_id=self.widget_type.id)

    def test_add_widget_to_page_as_admin(self):
        self.login_user(self.admin_user)
        self.app.post("/admin/page/{}/widget".format(self.page.slug),
                      data={"widgets": self.widget.id})
        page = self._get_model(Page, slug=self.page.slug)
        assert self.widget in page.widgets.all()

    def test_add_widget_to_page_as_non_admin(self):
        self.login_user(self.user1)
        response = self.app.post("/admin/page/{}/widget".format(self.page.slug),
                                 data={"widgets": self.widget.id})
        self.assertEquals(302, response.status_code)

    def test_add_widget_to_page_as_anonymous(self):
        response = self.app.post("/admin/page/{}/widget".format(self.page.slug),
                                 data={"widgets": self.widget.id})
        self.assertEquals(302, response.status_code)


class RemoveWidgetFromPageViewTest(AdminPageTest):
    def setUp(self):
        AdminPageTest.setUp(self)
        self.widget_type = self._create_model(
            WidgetType, name='poll')
        self.widget = self._create_model(
            Widget, name='test_widget',
            widget_type_id=self.widget_type.id)
        self.page.widgets.append(self.widget)
        db.session.commit()

    def test_remove_widget_from_page_as_admin(self):
        self.login_user(self.admin_user)
        assert self.widget in self.page.widgets
        self.app.get("/admin/page/{}/widget/{}/remove".
                     format(self.page.slug, self.widget.id))

        page = self._get_model(Page, slug=self.page.slug)
        widget = self._get_model(Widget, id=self.widget.id)
        assert widget is not None
        assert widget not in page.widgets

    def test_remove_widget_from_page_as_non_admin(self):
        self.login_user(self.user1)
        response = self.app.get("/admin/page/{}/widget/{}/remove".
                                format(self.page.slug, self.widget.id))
        self.assertEquals(302, response.status_code)

    def test_remove_widget_from_page_as_anonymous(self):
        response = self.app.get("/admin/page/{}/widget/{}/remove".
                                format(self.page.slug, self.widget.id))
        self.assertEquals(302, response.status_code)


class ShowPagePreviewViwewTest(AdminPageTest):
    def test_show_preview_as_admin(self):
        self.login_user(self.admin_user)
        response = self.app.get('/admin/page/preview/{}'.format(self.page.slug))
        self.assertEquals(200, response.status_code)

    def test_show_preview_as_non_admin(self):
        self.login_user(self.user1)
        response = self.app.get('/admin/page/preview/{}'.format(self.page.slug))
        self.assertEquals(302, response.status_code)

    def test_show_preview_as_anonymous(self):
        response = self.app.get('/admin/page/preview/{}'.format(self.page.slug))
        self.assertEquals(302, response.status_code)


class PublishPageViewTest(AdminPageTest):
    def test_publish_as_admin(self):
        self.login_user(self.admin_user)
        self.app.post("/admin/page/publish/{}".format(self.page.slug))
        page = self._get_model(Page, slug=self.page.slug)
        assert page.publish


class UnPublishPageViewTest(AdminPageTest):
    def test_unpublish_as_admin(self):
        self.login_user(self.admin_user)
        page = self._create_page(
            slug='fu', title='parent',
            description='description',
            level=0,
            publish=True, )
        assert page.publish
        self.app.post("/admin/page/unpublish/{}".format(page.slug))
        page = self._get_model(Page, slug=page.slug)
        assert not page.publish
