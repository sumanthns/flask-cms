from flask_cms.admin import admin
from flask_cms.admin.page.views import EditPageView, \
    AddPageView, DeletePageView, AddWidgetToPageView, RemoveWidgetFromPageView, ShowPagePreviewView
from flask_cms.admin.template.views import EditTemplateView, \
    AddTemplateView, DeleteTemplateView
from flask_cms.admin.views import IndexView
from flask_cms.admin.widget.views import \
    CreateWidgetView, ShowWidgetView, DeleteWidgetView,\
    WidgetIndexView

routes = [((admin,),
           ('', IndexView.as_view('index')),
           ('/page/<slug>', EditPageView.as_view('edit_page')),
           ('/page/<slug>/delete', DeletePageView.as_view('delete_page')),
           ('/page', AddPageView.as_view('add_page')),
           ('/page/preview/<slug>', ShowPagePreviewView.as_view('preview')),
           ('/template/<_id>', EditTemplateView.as_view('edit_template')),
           ('/template', AddTemplateView.as_view('add_template')),
           ('/template/<_id>/delete', DeleteTemplateView.as_view(
               'delete_template')),
           ('/widget', CreateWidgetView.as_view('create_widget')),
           ('/widget/<widget_id>', ShowWidgetView.as_view('show_widget')),
           ('/widget/<widget_id>/delete',
            DeleteWidgetView.as_view('delete_widget')),
           ('/widget/list', WidgetIndexView.as_view('list_widget')),
           ('/page/<slug>/widget', AddWidgetToPageView.as_view('add_widget_to_page')),
           ('/page/<slug>/widget/<widget_id>/remove',
            RemoveWidgetFromPageView.as_view('remove_widget_from_page')), )]
