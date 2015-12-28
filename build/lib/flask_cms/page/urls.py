from flask_cms.page import page
from flask_cms.page.views import PageView

routes = [((page,),
           ('/<slug>', PageView.as_view('show')), )]
