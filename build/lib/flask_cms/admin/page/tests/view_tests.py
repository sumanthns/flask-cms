from flask_cms.testing import TestCase


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
        self.page = self._create_page(
            slug='test', title='title',
            description='description'
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
        self.login_user(self.admin_user)
        self.app.post("/admin/page/test",
                      data={
                          'slug': 'fu',
                          'title': 'bar',
                      })
        page = self._get_page(slug='fu')
        assert page
        self.assertFalse(page.login_required)
        self.assertEquals('bar', page.title)

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


class AddPageTest(AdminPageTest):
    def test_post_as_admin(self):
        self.login_user(self.admin_user)
        self.app.post("/admin/page",
                      data={
                          'slug': 'fu',
                          'title': 'bar',
                          'description': 'desc',
                          'login_required': True,
                          'publish': True,
                      })
        page = self._get_page(slug='fu')
        assert page
        assert page.login_required
        assert page.publish
        assert page.created_at is not None
        self.assertEquals(0, page.level)
        self.assertEquals('bar', page.title)
        self.assertEquals('desc', page.description)

    def test_post_as_admin_with_parent(self):
        self.parent = self._create_page(
            slug='parent', title='parent',
            description='description',
            level=0,
        )
        self.login_user(self.admin_user)
        self.app.post("/admin/page",
                      data={
                          'slug': 'fu',
                          'title': 'bar',
                          'description': 'desc',
                          'login_required': True,
                          'parent_slug': 'parent'
                      })
        page = self._get_page(slug='fu')
        assert page
        assert page.login_required
        self.assertEquals(1, page.level)
        self.assertEquals('bar', page.title)
        self.assertEquals('desc', page.description)
        self.assertEquals(page.parent, self.parent)

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
