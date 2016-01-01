from flask_cms.member import member
from flask_cms.member.views import MemberView, ChangePasswordView, OtherMemberView

routes = [((member,),
           ('', MemberView.as_view('show')),
           ('/<member_id>', OtherMemberView.as_view('member_show')),
           ('/change_password',
            ChangePasswordView.as_view('change_password')),)]
