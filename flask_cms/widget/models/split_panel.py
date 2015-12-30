from flask_cms.ext import db


class SplitPanel(db.Model):
    __tablename__ = "split_panels"
    id = db.Column(db.Integer, primary_key=True)
    widget_id = db.Column(db.Integer, db.ForeignKey('widgets.id'))
    type = db.Column(db.String(255))
    link = db.Column(db.String(255))
    align = db.Column(db.String(255))
    size = db.Column(db.String(255))
    title = db.Column(db.String(255))
    content = db.Column(db.String(1024))
    widget = db.relationship("Widget",
                             backref=db.backref(
                                 "split_panel", cascade='delete',
                                 uselist=False))

    @staticmethod
    def create_by_form(form):
        split_panel = SplitPanel(
            title=form.title.data,
            content=form.content.data,
            type=form.multimedia_types.data,
            link=form.link.data,
            size=form.size.data,
            align=form.align.data,
        )
        return split_panel
