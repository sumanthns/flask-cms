# flask-cms

## Installation

python setup.py install

## To run tests

./run_tests.sh

## To run database migration

1. Create a mysql database locally, called flaskcms
To change the database name or database server - Edit SQLALCHEMY_DATABASE_URI for DevelopmentConfig in flask_cms/settings.py
2. Run, python flask_cms/manage.py db upgrade

## Create a test users

python flask_cms/manage.py setup
(This will create an admin and non-admin user in development db)

## To run local server

./run.sh

## To access admin portal

http://localhost:5000/admin

# Description

This is a CMS based on flask. This provides a admin interface to create pages, templates, widgets etc.


## Page

1. A page can also have a children.
2. A page can be protected by making it require a login to visit
3. Admins can preview the page before publishing it.
4. Only parent pages can be made to show on nav bar

## Templates

The apps comes with some pre-defined templates
1. notice_board_template
This will show descriptions of all child pages of a given page like stickies on a notice board

2. blog_template

This will show a page with a header image and a rich text description below it, in a blog manner

### To add a new template

1. Admins should create a template with a name, say my_new_template from admin console
2. Create a html file with the same in flask_cms/page/templates
  Create - flask_cms/page/templates/my_new_template.html
3. The html file should be a macro called render_page, that can take in a "page" parameter

# Widgets

1. There are some pre-defined widgets in the system
carousel - image scroller
map
poll
grid - (which shows page descriptions in a grid like manner. There is 1 * 3 grid existing in the system)

2. Admins can drop these widgets on pages, which will show up on these pages

## To add a new widget

1.  Create a widget type from admin console
2. add a create form template to be able to create new widget of this type
To create a new widget of type - my_new_widget_type
create flask_cms/admin/templates/my_new_widget_type/create_my_new_widget_type_form.html.
This should define the admin form about what all it requires to create a new widget.

create flask_cms/admin/templates/my_new_widget_type/show_my_new_widget_type.html
This is to define how admin can see widgets of this new type.

3. After create a new widget, it should be available on page view for admins, so that
admins can drop these widgets on any page.

4. You should also define a html template to define how the widget should look like
when dropped on a page.

To control how a widget, my_new_widget should look like on a page

create flask_cms/widget/templates/widget/my_new_widget.html

This html template should be a macro called render_widget, which takes in two parameter, component and page
component - widget object
page - page on which the widget is dropped
