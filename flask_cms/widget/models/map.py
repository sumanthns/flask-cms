from flask_cms.ext import db


class Map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    widget_id = db.Column(db.Integer, db.ForeignKey('widgets.id'))
    widget = db.relationship("Widget",
                             backref=db.backref(
                                 "map", cascade='delete',
                                 uselist=False))
    address = db.Column(db.UnicodeText)
    longitude = db.Column(db.String(64))
    latitude = db.Column(db.String(64))
    title = db.Column(db.String(64))

    @staticmethod
    def create_by_form(form):
        map = Map(
            title=form.title.data,
            address=form.address.data,
            latitude=form.latitude.data,
            longitude=form.longitude.data,
        )
        return map
