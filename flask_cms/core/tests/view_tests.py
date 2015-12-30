from flask_cms.testing import TestCase


class IndexViewTest(TestCase):
    def test_get(self):
        response = self.app.get("/")
        self.assertEquals(302, response.status_code)
