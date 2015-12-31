from flask_cms.testing import TestCase


class PageViewTest(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.user1 = self._create_user(
            email='fu@bar.com', password='password',
            active=True)
        self.template = self._create_template(
            name='notice_board_template',
            description='fubar'
        )
        self.page = self._create_page(
            slug='test', title='title',
            description='description',
            publish=True,
            template_id=self.template.id,
        )
        self.page_require_login = self._create_page(
            slug='test_login', title='title',
            description='description',
            login_required=True,
            publish=True,
            template_id=self.template.id,
        )
        self.unpublished_page = self._create_page(
            slug='test_publish', title='title',
            description='description',
            login_required=True,
            template_id=self.template.id,
        )

    def test_get(self):
        response = self.app.get("/page/test")

        self.assertEquals(response.status_code, 200)

    def test_get_protects_pages_require_login(self):
        response = self.app.get("/page/test_login")

        self.assertEquals(response.status_code, 302)

    def test_get_protects_unpublished_page(self):
        self.login_user(self.user1)
        response = self.app.get("/page/test_publish")

        self.assertEquals(response.status_code, 404)

    def test_get_page_with_login(self):
        self.login_user(self.user1)
        response = self.app.get("/page/test_login")

        self.assertEquals(response.status_code, 200)
