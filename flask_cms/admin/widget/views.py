from flask import render_template, url_for, flash, request
from werkzeug.utils import redirect

from flask_cms.admin.views import AdminView
from flask_cms.admin.widget.forms import WidgetFormFactory, WidgetTypeForm
from flask_cms.ext import db
from flask_cms.utils import get_object_or_404, flash_errors
from flask_cms.widget.models.widget import Widget
from flask_cms.widget.models.widget_type import WidgetType


class CreateWidgetView(AdminView):
    def get(self):
        type = request.args.get('type', None)
        form = WidgetFormFactory(type=type).get_widget_form()
        if type is not None:
            return render_template(
                "widget/{}/create_{}_widget_form.html".format(type, type),
                form=form)
        else:
            return render_template("widget/widget.html", form=form)

    def post(self):
        widget_type_id = int(request.form.get('types'))
        widget_type = get_object_or_404(
            WidgetType, WidgetType.id == widget_type_id)
        form = WidgetFormFactory(
            type=widget_type.name).get_widget_form()

        if form.validate_on_submit():
            widget = Widget(
                name=form.name.data,
                widget_type_id=int(form.types.data)
            )
            db.session.add(widget)
            db.session.commit()
            component = widget.get_component_class()
            component = component.create_by_form(form)
            component.widget = widget
            db.session.add(component)
            db.session.commit()
            flash("Successfully created widget - {}".format(widget.name))
            return redirect(url_for('admin.list_widget'))
        return render_template('widget/widget.html', form=form)


class DeleteWidgetView(AdminView):
    def get(self, widget_id):
        widget = get_object_or_404(Widget, Widget.id == widget_id)
        db.session.delete(widget)
        db.session.commit()
        flash("Successfully deleted widget - {}".format(widget.name))
        return redirect(url_for('admin.list_widget'))


class ShowWidgetView(AdminView):
    def get(self, widget_id):
        widget = get_object_or_404(Widget, Widget.id == widget_id)
        widget_name = widget.widget_type.name
        component = widget.get_component()
        if component is None:
            flash("Widget is empty", "error")
            return redirect(url_for('admin.list_widget'))

        return render_template("widget/{}/show_{}_widget.html".
                               format(widget_name, widget_name),
                               widget=widget,
                               component=component)


class WidgetIndexView(AdminView):
    def get(self):
        widgets = Widget.query.all()
        widget_types = WidgetType.query.all()
        return render_template("widget/list_widget.html",
                               widgets=widgets, widget_types=widget_types)


class CreateWidgetTypeView(AdminView):
    def get(self):
        form = WidgetTypeForm()
        return render_template("widget_type/create_widget_type.html", form=form)

    def post(self):
        form = WidgetTypeForm()
        if form.validate_on_submit():
            widget_type = WidgetType(name=form.name.data)
            db.session.add(widget_type)
            db.session.commit()
            flash("Widget type - {} successfully created".format(widget_type.name))
            return redirect(url_for('admin.list_widget'))

        flash_errors(form)
        return render_template("widget_type/create_widget_type.html", form=form)


class DeleteWidgetTypeView(AdminView):
    def get(self, widget_type_id):
        widget_type = get_object_or_404(WidgetType, WidgetType.id == widget_type_id)
        db.session.delete(widget_type)
        db.session.commit()
        flash("Successfully deleted widget_type - {}".format(widget_type.name))
        return redirect(url_for('admin.list_widget'))
