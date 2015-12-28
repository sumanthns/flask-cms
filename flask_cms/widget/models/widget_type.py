from flask_cms.ext import db


class WidgetType(db.Model):
    __tablename__ = "widget_types"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    widgets = db.relationship('Widget', backref='widget_type', lazy='dynamic')
