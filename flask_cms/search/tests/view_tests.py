from flask_cms.app.models.users import User
from flask_cms.ext import db
from flask_cms.page.models import Page
from flask_cms.search.views import SearchView
from flask_cms.testing import TestCase


class SearchViewTest(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.user1 = self._create_model(
            User,
            first_name="User 1",
            last_name="User 1 last name",
            email="fu.bar@gmail.com")
        self.user2 = self._create_model(
            User,
            first_name="User 2",
            last_name="User 2 last name",
            email="ku.kar@gmail.com")
        self.page1 = self._create_model(
            Page,
            title="title1",
            description='description1',
            content=unicode('content1'),
            slug="page1",
        )
        self.page2 = self._create_model(
            Page,
            title="title2",
            description='description2',
            content=unicode('content2'),
            slug="page2",
        )

    def test_get_with_empty_keyword(self):
        response = self.app.get("/search?q=")
        self.assertEquals(404, response.status_code)
        response = self.app.get("/search?q=     ")
        self.assertEquals(404, response.status_code)

    def test_get_with_keyword(self):
        response = self.app.get("/search?q=title")
        self.assertEquals(200, response.status_code)

    def test_get_with_unique_keyword_for_pages(self):
        results = SearchView()._get_search_results("title1")
        expected_results = [
            (self.page1.title, self.page1.description, self.page1.slug), ]
        self.assertEquals(expected_results, results["pages"])

        results = SearchView()._get_search_results("description2")
        expected_results = [
            (self.page2.title, self.page2.description, self.page2.slug), ]
        self.assertEquals(expected_results, results["pages"])

        results = SearchView()._get_search_results("content2")
        expected_results = [
            (self.page2.title, self.page2.description, self.page2.slug), ]
        self.assertEquals(expected_results, results["pages"])

    def test_get_with_common_keyword_for_pages(self):
        results = SearchView()._get_search_results("title")
        expected_results = [
            (self.page1.title, self.page1.description, self.page1.slug),
            (self.page2.title, self.page2.description, self.page2.slug), ]
        self.assertEquals(expected_results, results["pages"])

        results = SearchView()._get_search_results("description")
        expected_results = [
            (self.page1.title, self.page1.description, self.page1.slug),
            (self.page2.title, self.page2.description, self.page2.slug), ]
        self.assertEquals(expected_results, results["pages"])

    def test_get_with_unique_keyword_for_user(self):
        results = SearchView()._get_search_results("User 1")
        expected_results = [
            (self.user1.first_name, self.user1.last_name, self.user1.email, self.user1.id), ]
        self.assertEquals(expected_results, results["users"])

        results = SearchView()._get_search_results("User 2 last name")
        expected_results = [
            (self.user2.first_name, self.user2.last_name, self.user2.email, self.user2.id), ]
        self.assertEquals(expected_results, results["users"])

        results = SearchView()._get_search_results("kar")
        expected_results = [
            (self.user2.first_name, self.user2.last_name, self.user2.email, self.user2.id), ]
        self.assertEquals(expected_results, results["users"])

    def test_get_with_common_keyword_for_user(self):
        results = SearchView()._get_search_results("User")
        expected_results = [
            (self.user1.first_name, self.user1.last_name, self.user1.email, self.user1.id),
            (self.user2.first_name, self.user2.last_name, self.user2.email, self.user2.id), ]
        self.assertEquals(expected_results, results["users"])

    def test_get_with_common_keyword_in_bot_user_and_pages(self):
        self.page1.description = "user"
        db.session.commit()

        results = SearchView()._get_search_results("User")
        expected_user_results = [
            (self.user1.first_name, self.user1.last_name, self.user1.email, self.user1.id),
            (self.user2.first_name, self.user2.last_name, self.user2.email, self.user2.id), ]
        self.assertEquals(expected_user_results, results["users"])

        expected_page_results = [
            (self.page1.title, self.page1.description, self.page1.slug), ]
        self.assertEquals(expected_page_results, results["pages"])
