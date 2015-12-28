from werkzeug.utils import import_string
from flask_cms.ext import db
from flask_cms.page.models import PageWidget


class WidgetNotSupportedException(Exception):
    pass


class Widget(db.Model):
    __tablename__ = "widgets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    widget_type_id = db.Column(db.Integer, db.ForeignKey('widget_types.id'))
    pages_widgets = db.relationship("PageWidget", cascade='delete')

    def get_component(self):
        component_name = self.widget_type.name

        if component_name is None:
            raise WidgetNotSupportedException("Widget does not have a widget type")

        from flask_cms.app import app

        for wm in app.config.get("WIDGET_MODELS", []):
            widget_type, model = wm
            if component_name == widget_type:
                model = import_string(model)
                existing_model = model.query.filter_by(widget_id=self.id).first()
                if existing_model is not None:
                    return existing_model
                else:
                    return model

        raise WidgetNotSupportedException("Widget {} is not supported".format(component_name))
