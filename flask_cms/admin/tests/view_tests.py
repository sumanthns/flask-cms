from flask_cms.admin.page.tests.view_tests import AdminPageTest


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
