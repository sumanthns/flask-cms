from flask_cms.testing import TestCase


class AdminTemplateTest(TestCase):
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
            name='test', description='description',
        )


class EditTemplateViewTest(AdminTemplateTest):
    def test_get_as_admin(self):
        self.login_user(self.admin_user)
        response = self.app.get("/admin/template/{}".format(self.template.id))

        self.assertEquals(response.status_code, 200)

    def test_get_as_non_admin(self):
        self.login_user(self.user1)
        response = self.app.get("/admin/template/{}".format(self.template.id))

        self.assertEquals(response.status_code, 302)

    def test_get_as_anonymous(self):
        response = self.app.get("/admin/template/{}".format(self.template.id))

        self.assertEquals(response.status_code, 302)

    def test_post_as_admin(self):
        self.login_user(self.admin_user)
        self.app.post("/admin/template/{}".format(self.template.id),
                      data={
                          'name': 'fu',
                          'description': 'bar', })
        template = self._get_template(id=self.template.id)
        self.assertEquals('fu', template.name)
        self.assertEquals('bar', template.description)

    def test_post_as_non_admin(self):
        self.login_user(self.user1)
        response = self.app.post("/admin/template/{}".format(self.template.id),
                                 data={
                                     'name': 'fu',
                                     'description': 'bar', })
        self.assertEquals(response.status_code, 302)

    def test_post_as_anonymous(self):
        response = self.app.post("/admin/template/{}".format(self.template.id),
                                 data={
                                     'name': 'fu',
                                     'description': 'bar', })
        self.assertEquals(response.status_code, 302)


class DeleteTemplateViewTest(AdminTemplateTest):
    def test_delete_as_admin(self):
        template = self._create_template(
            name='fu',
            description='description',
        )
        assert self._get_template(name="fu")
        self.login_user(self.admin_user)
        self.app.get("/admin/template/{}/delete".format(template.id))
        assert self._get_template(name='fu') is None

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


class AddTemplateViewTest(AdminTemplateTest):
    def test_post_as_admin(self):
        self.login_user(self.admin_user)
        self.app.post("/admin/template",
                      data={
                          'name': 'fu',
                          'description': 'desc',
                      })
        template = self._get_template(name='fu')
        assert template
        self.assertEquals('desc', template.description)

    def test_post_as_non_admin(self):
        self.login_user(self.user1)
        response = self.app.post("/admin/template",
                                 data={
                                     'name': 'fu',
                                     'title': 'bar',
                                 })
        self.assertEquals(response.status_code, 302)

    def test_post_as_anonymous(self):
        response = self.app.post("/admin/template",
                                 data={
                                     'name': 'fu',
                                     'title': 'bar',
                                 })
        self.assertEquals(response.status_code, 302)
