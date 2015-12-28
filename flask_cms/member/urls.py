from flask_cms.member import member
from flask_cms.member.views import MemberView, ChangePasswordView

routes = [((member,),
           ('', MemberView.as_view('show')),
           ('/change_password',
            ChangePasswordView.as_view('change_password')),)]
