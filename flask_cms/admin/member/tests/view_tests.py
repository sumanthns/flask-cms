from flask_cms.app.models.roles import Role
from flask_cms.app.models.users import User
from flask_cms.testing import TestCase


class AdminMemberTest(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.admin_user = self._create_admin_user(
            email="admin@admin.com",
            password="password",
            active=True)
        self.member_role = self._create_model(
            Role,
            name='member',
            description='member', )
        self.member_user = self._create_model(
            User,
            email="member@member.com",
            password="password",
            roles=[self.member_role])
        self.admin_role = self._get_model(
            Role, name="admin", )

    def test_admin_can_create_member(self):
        self.login_user(self.admin_user)
        self.app.post("/admin/member",
                      data={
                          'first_name': "fu",
                          'last_name': "bar",
                          'email': "fu@bar.com",
                          'roles': [self.member_role.id], })
        member = self._get_model(User,
                                 email="fu@bar.com")
        assert member
        self.assertEquals("fu", member.first_name)
        self.assertEquals("bar", member.last_name)
        assert self.member_role in member.roles

    def test_admin_edit_member(self):
        self.login_user(self.admin_user)
        self.app.post("/admin/member/{}".format(self.member_user.id),
                      data={
                          'first_name': "fu",
                          'last_name': "bar",
                          'email': "fu@bar.com",
                          'roles': [self.member_role.id, self.admin_role.id], })
        member = self._get_model(User, id=self.member_user.id)
        assert member
        self.assertEquals("fu", member.first_name)
        self.assertEquals("bar", member.last_name)
        assert self.member_role in member.roles
        assert self.admin_role in member.roles

    def test_admin_can_delete_member(self):
        self.login_user(self.admin_user)
        self.app.get("/admin/member/{}/delete".format(self.member_user.id))
        member = self._get_model(User, id=self.member_user.id)
        assert member is None

    def test_admin_can_create_and_delete_role(self):
        self.login_user(self.admin_user)
        self.app.post("/admin/role",
                      data={
                          "name": "fu",
                          "description": "fubar", })
        role = self._get_model(Role, name="fu")
        assert role
        self.assertEquals("fubar", role.description)

        self.app.get("/admin/role/{}/delete".format(role.id))
        role = self._get_model(Role, name="fu")
        assert role is None

    def test_non_admin_cannot_create_member(self):
        self.login_user(self.member_user)
        response = self.app.post("/admin/member",
                                 data={
                                     'first_name': "fu",
                                     'last_name': "bar",
                                     'email': "fu@bar.com",
                                     'roles': [self.member_role.id], })
        self.assertEquals(302, response.status_code)
        member = self._get_model(User,
                                 email="fu@bar.com")
        assert member is None

    def test_anonymous_user_cannot_create_member(self):
        response = self.app.post("/admin/member",
                                 data={
                                     'first_name': "fu",
                                     'last_name': "bar",
                                     'email': "fu@bar.com",
                                     'roles': [self.member_role.id], })
        self.assertEquals(302, response.status_code)
        member = self._get_model(User,
                                 email="fu@bar.com")
        assert member is None

    def test_non_admin_cannot_edit_member(self):
        self.login_user(self.member_user)
        response = self.app.post("/admin/member/{}".format(self.member_user.id),
                                 data={
                                     'email': "fu@bar.com", })
        self.assertEquals(302, response.status_code)
        member = self._get_model(User,
                                 email="fu@bar.com")
        assert member is None

        member = self._get_model(User, id=self.member_user.id)
        self.assertEquals("member@member.com", member.email)

    def test_anonymous_user_cannot_edit_member(self):
        response = self.app.post("/admin/member/{}".format(self.member_user.id),
                                 data={
                                     'email': "fu@bar.com", })
        self.assertEquals(302, response.status_code)
        member = self._get_model(User,
                                 email="fu@bar.com")
        assert member is None

        member = self._get_model(User, id=self.member_user.id)
        self.assertEquals("member@member.com", member.email)

    def test_non_admin_cannot_delete_member(self):
        self.login_user(self.member_user)
        response = self.app.get("/admin/member/{}/delete".format(self.member_user.id))
        self.assertEquals(302, response.status_code)
        member = self._get_model(User, id=self.member_user.id)
        assert member

    def test_anonymous_user_cannot_delete_member(self):
        response = self.app.get("/admin/member/{}/delete".format(self.member_user.id))
        self.assertEquals(302, response.status_code)
        member = self._get_model(User, id=self.member_user.id)
        assert member

    def test_non_admin_cannot_create_role(self):
        self.login_user(self.member_user)
        response = self.app.post("/admin/role",
                                 data={
                                     "name": "fu",
                                     "description": "fubar", })
        self.assertEquals(302, response.status_code)
        role = self._get_model(Role, name="fu")
        assert role is None

    def test_anonymous_user_cannot_create_role(self):
        response = self.app.post("/admin/role",
                                 data={
                                     "name": "fu",
                                     "description": "fubar", })
        self.assertEquals(302, response.status_code)
        role = self._get_model(Role, name="fu")
        assert role is None

    def test_non_admin_cannot_delete_role(self):
        self.login_user(self.member_user)
        response = self.app.get("/admin/role/{}/delete".format(self.member_role.id))
        self.assertEquals(302, response.status_code)

        role = self._get_model(Role, id=self.member_role.id)
        assert role

    def test_anonymous_user_cannot_delete_role(self):
        response = self.app.get("/admin/role/{}/delete".format(self.member_role.id))
        self.assertEquals(302, response.status_code)

        role = self._get_model(Role, id=self.member_role.id)
        assert role
