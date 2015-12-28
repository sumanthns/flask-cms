from flask_cms.testing import TestCase


class MemberViewTest(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.user1 = self._create_user(
            email='fu@bar.com', password='password',
            active=True)

    def test_get_should_redirect_if_not_logged_in(self):
        response = self.app.get("/member")

        self.assertEquals(response.status_code, 302)
        assert "/login" in response.location

    def test_post_should_redirect_if_not_logged_in(self):
        response = self.app.post("/member")

        self.assertEquals(response.status_code, 302)
        assert "/login" in response.location

    def test_should_show_user_details_of_logged_in_user(self):
        self.login_user(self.user1)
        response = self.app.get("/member")

        self.assertEquals(response.status_code, 200)
        assert self.user1.email in response.data

    def test_logged_in_user_can_update_with_full_details(self):
        self.login_user(self.user1)
        self.app.post("/member",
                      data={'first_name': "fu",
                            'last_name': "bar",
                            'email': self.user1.email})
        user = self._get_user(email=self.user1.email)

        self.assertEquals("fu", user.first_name)
        self.assertEquals("bar", user.last_name)

    def test_logged_in_user_no_update_without_full_details(self):
        self.login_user(self.user1)
        self.app.post("/member",
                      data={'first_name': "fu",
                            'last_name': "bar", })
        user = self._get_user(email=self.user1.email)

        self.assertEquals(None, user.first_name)
        self.assertEquals(None, user.last_name)


class ChangePasswordTest(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.user1 = self._create_user(
            email='fu@bar.com', password='password',
            active=True)

    def test_get_login_required(self):
        response = self.app.get('/member/change_password')

        self.assertEquals(response.status_code, 302)
        assert "/login" in response.location

    def test_post_login_required(self):
        response = self.app.post('/member/change_password')

        self.assertEquals(response.status_code, 302)
        assert "/login" in response.location

    def test_logged_in_user_change_password(self):
        self.login_user(self.user1)
        self.app.post('/member/change_password',
                      data={"password": 'Password1',
                            "confirm_password": 'Password1'})

        user = self._get_user(email=self.user1.email)
        assert self._verify_password('Password1', user.password)

    def test_logged_in_user_cannot_change_password_without_all_details(self):
        self.login_user(self.user1)
        self.app.post('/member/change_password',
                      data={"password": 'Password1', })

        user = self._get_user(email=self.user1.email)
        assert self._verify_password(self.user1.password, user.password)

    def test_logged_in_user_cannot_change_password_without_matching_passwords(self):
        self.login_user(self.user1)
        self.app.post('/member/change_password',
                      data={"password": 'Password1',
                            "confirm_password": "password"})

        user = self._get_user(email=self.user1.email)
        assert self._verify_password(self.user1.password, user.password)
