from flask_cms.testing import TestCase
from flask_cms.widget.models.poll import Poll, Choice
from flask_cms.widget.models.widget import Widget
from flask_cms.widget.models.widget_type import WidgetType


class PollViewTest(TestCase):
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
            login_required=True,
        )
        self.widget_type = self._create_model(
            WidgetType, name='poll', )
        self.widget = self._create_model(
            Widget, name='test_poll',
            widget_type_id=self.widget_type.id,
        )
        self.poll = self._create_model(
            Poll, question="test_question",
            widget_id=self.widget.id,
        )
        self.choice1 = self._create_model(
            Choice, description="fu",
            vote=0
        )
        self.choice2 = self._create_model(
            Choice, description="bar",
            vote=0
        )

    def test_vote(self):
        self.login_user(self.user1)
        self.app.post("/widget/page/{}/poll/{}".
                      format(self.page.slug, self.widget.id),
                      data={"choice": self.choice1.id})
        choice = self._get_model(Choice, id=self.choice1.id)
        self.assertEquals(1, choice.vote)
        self.app.post("/widget/page/{}/poll/{}".
                      format(self.page.slug, self.widget.id),
                      data={"choice": self.choice1.id})
        choice = self._get_model(Choice, id=self.choice1.id)
        self.assertEquals(2, choice.vote)
        self.app.post("/widget/page/{}/poll/{}".
                      format(self.page.slug, self.widget.id),
                      data={"choice": self.choice2.id})
        choice = self._get_model(Choice, id=self.choice2.id)
        self.assertEquals(1, choice.vote)

    def test_vote_as_anonymous(self):
        response = self.app.post("/widget/page/{}/poll/{}".
                                 format(self.page.slug, self.widget.id),
                                 data={"choice": self.choice1.id})
        self.assertEquals(404, response.status_code)
