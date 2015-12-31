from flask_cms.ext import db
from flask_cms.page.models import Page


class GridPage(db.Model):
    __tablename__ = "grid_pages"
    id = db.Column(db.Integer, primary_key=True)
    grid_id = db.Column(db.Integer, db.ForeignKey('grids.id'))
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'))


class Grid(db.Model):
    __tablename__ = "grids"
    id = db.Column(db.Integer, primary_key=True)
    widget_id = db.Column(db.Integer, db.ForeignKey('widgets.id'))
    widget = db.relationship("Widget",
                             backref=db.backref(
                                 "grid", cascade='delete',
                                 uselist=False))
    grid_type = db.Column(db.String(255))
    pages = db.relationship("Page", secondary=GridPage.__tablename__)
    grid_pages = db.relationship("GridPage", cascade="delete,all")

    @staticmethod
    def create_by_form(form):
        grid = Grid(
            grid_type=form.grid_types.data,
        )
        for grid_page in form.grid_pages:
            page = Page.query.filter_by(
                slug=grid_page.page_slug.data).first()
            grid.pages.append(page)
        return grid
