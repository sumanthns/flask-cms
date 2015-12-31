from flask_cms.ext import db


class Carousel(db.Model):
    __tablename__ = "carousels"
    id = db.Column(db.Integer, primary_key=True)
    widget_id = db.Column(db.Integer, db.ForeignKey('widgets.id'))
    widget = db.relationship("Widget",
                             backref=db.backref(
                                 "carousel", cascade='delete',
                                 uselist=False))
    carousel_images = db.relationship("CarouselImage", backref="poll",
                                      lazy="dynamic", cascade="delete,all")

    @staticmethod
    def create_by_form(form):
        carousel = Carousel()
        carousel.carousel_images = []
        for image in form.images:
            carousel_image = CarouselImage(
                image_link=image.image_link.data,
                image_caption=image.image_caption.data,
                image_description=image.image_description.data,
            )
            carousel.carousel_images.append(carousel_image)
        return carousel


class CarouselImage(db.Model):
    __tablename__ = "carousel_images"
    id = db.Column(db.Integer, primary_key=True)
    carousel_id = db.Column(db.Integer, db.ForeignKey('carousels.id'))
    image_link = db.Column(db.String(255))
    image_caption = db.Column(db.String(255))
    image_description = db.Column(db.String(255))
