from flask_cms.widget import widget
from flask_cms.widget.poll_views import PollVoteView

routes = [((widget,),
           ('/page/<slug>/poll/<widget_id>', PollVoteView.as_view('poll')), )]
