from flask_cms.admin import admin
from flask_cms.admin.page.views import EditPageView,\
    AddPageView, DeletePageView
from flask_cms.admin.template.views import EditTemplateView,\
    AddTemplateView, DeleteTemplateView
from flask_cms.admin.views import IndexView

routes = [((admin,),
           ('', IndexView.as_view('index')),
           ('/page/<slug>', EditPageView.as_view('edit_page')),
           ('/page/<slug>/delete', DeletePageView.as_view('delete_page')),
           ('/page', AddPageView.as_view('add_page')),
           ('/template/<_id>', EditTemplateView.as_view('edit_template')),
           ('/template', AddTemplateView.as_view('add_template')),
           ('/template/<_id>/delete', DeleteTemplateView.as_view(
               'delete_template')),)]
