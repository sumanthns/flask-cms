from sqlalchemy.orm import backref
from flask_cms.ext import db


class PageWidget(db.Model):
    __tablename__ = "pages_widgets"
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey("pages.id"))
    widget_id = db.Column(db.Integer, db.ForeignKey("widgets.id"))


class Page(db.Model):
    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(255), unique=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    header_image = db.Column(db.String(255))
    login_required = db.Column(db.Boolean, default=False)
    show_in_nav = db.Column(db.Boolean, default=False)
    publish = db.Column(db.Boolean, default=False)
    content = db.Column(db.UnicodeText)
    parent_id = db.Column(db.Integer, db.ForeignKey(id))
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'))
    level = db.Column(db.Integer)
    children = db.relationship('Page', backref=backref('parent', remote_side=[id]), cascade="delete",
                               lazy='dynamic')
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.now(), nullable=False)
    widgets = db.relationship("Widget", secondary=PageWidget.__tablename__,
                              lazy="dynamic", )
    pages_widgets = db.relationship("PageWidget", cascade='delete', )
    grid_pages = db.relationship("GridPage", cascade='delete', )

    def children_ordered_by_latest(self):
        return self.children.order_by(Page.created_at.desc()).all()
