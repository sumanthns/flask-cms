from flask_cms.admin import admin
from flask_cms.admin.member.views import CreateMemberView, EditMemberView, DeleteMemberView, MemberListView, \
    CreateRoleView, DeleteRoleView
from flask_cms.admin.page.views import EditPageView, \
    AddPageView, DeletePageView, AddWidgetToPageView, RemoveWidgetFromPageView, ShowPagePreviewView, PublishPageView, \
    UnPublishPageView
from flask_cms.admin.template.views import EditTemplateView, \
    AddTemplateView, DeleteTemplateView
from flask_cms.admin.views import IndexView
from flask_cms.admin.widget.views import \
    CreateWidgetView, ShowWidgetView, DeleteWidgetView,\
    WidgetIndexView, CreateWidgetTypeView, DeleteWidgetTypeView

routes = [((admin,),
           ('', IndexView.as_view('index')),
           ('/page/<slug>', EditPageView.as_view('edit_page')),
           ('/page/<slug>/delete', DeletePageView.as_view('delete_page')),
           ('/page', AddPageView.as_view('add_page')),
           ('/page/preview/<slug>', ShowPagePreviewView.as_view('preview')),
           ('/page/publish/<slug>', PublishPageView.as_view('publish_page')),
           ('/page/unpublish/<slug>', UnPublishPageView.as_view('unpublish_page')),
           ('/template/<_id>', EditTemplateView.as_view('edit_template')),
           ('/template', AddTemplateView.as_view('add_template')),
           ('/template/<_id>/delete', DeleteTemplateView.as_view(
               'delete_template')),
           ('/widget', CreateWidgetView.as_view('create_widget')),
           ('/widget/<widget_id>', ShowWidgetView.as_view('show_widget')),
           ('/widget/<widget_id>/delete',
            DeleteWidgetView.as_view('delete_widget')),
           ('/widget/list', WidgetIndexView.as_view('list_widget')),
           ('/widget_type', CreateWidgetTypeView.as_view('create_widget_type')),
           ('/widget_type/delete/<widget_type_id>', DeleteWidgetTypeView.as_view('delete_widget_type')),
           ('/page/<slug>/widget', AddWidgetToPageView.as_view('add_widget_to_page')),
           ('/page/<slug>/widget/<widget_id>/remove',
            RemoveWidgetFromPageView.as_view('remove_widget_from_page')),
           ('/member', CreateMemberView.as_view('create_member')),
           ('/member/<member_id>', EditMemberView.as_view('edit_member')),
           ('/member/<member_id>/delete', DeleteMemberView.as_view('delete_member')),
           ('/members', MemberListView.as_view('list_member')),
           ('/role', CreateRoleView.as_view('create_role')),
           ('/role/<role_id>/delete', DeleteRoleView.as_view('delete_role')), )]
