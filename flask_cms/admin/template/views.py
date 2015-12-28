from flask import render_template, url_for, request, flash
from werkzeug.utils import redirect
from flask_cms.admin.template.forms import TemplateForm
from flask_cms.admin.template.models import Template
from flask_cms.admin.views import AdminView
from flask_cms.ext import db
from flask_cms.utils import get_object_or_404


class AddTemplateView(AdminView):
    def get(self):
        form = TemplateForm()
        return render_template("template/template.html", form=form)

    def post(self):
        form = TemplateForm()
        if form.validate_on_submit():
            template = Template(name=form.name.data,
                                description=form.description.data)
            db.session.add(template)
            db.session.commit()
            return redirect(url_for('admin.edit_template', _id=template.id))
        return render_template("template/template.html", form=form)


class EditTemplateView(AdminView):
    def get(self, _id):
        template = get_object_or_404(Template, Template.id == _id)
        form = TemplateForm(template)
        return render_template("template/template.html", form=form)

    def post(self, _id):
        template = get_object_or_404(Template, Template.id == _id)
        form = TemplateForm(template)
        if form.validate_on_submit():
            template.name = request.form.get('name')
            template.description = request.form.get('description')
            db.session.commit()
            return redirect(url_for('admin.edit_template', _id=template.id))
        return render_template("template/template.html", form=form)


class DeleteTemplateView(AdminView):
    def get(self, _id):
        template = get_object_or_404(Template, Template.id == _id)
        db.session.delete(template)
        db.session.commit()
        flash("Succesfully deleted template - {}".format(template.name))
        return redirect(url_for('admin.index'))
