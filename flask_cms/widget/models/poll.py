from flask_cms.ext import db


class Poll(db.Model):
    __tablename__ = "polls"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), unique=True)
    widget_id = db.Column(db.Integer, db.ForeignKey('widgets.id'))
    widget = db.relationship("Widget",
                             backref=db.backref(
                                 "poll", cascade='delete',
                                 uselist=False))
    choices = db.relationship("Choice", backref="poll",
                              lazy="dynamic", cascade="delete,all")

    @staticmethod
    def create_by_form(form):
        poll = Poll(
            question=form.question.data
        )
        choice1 = Choice(
            description=form.choice1.data,
            vote=0, )
        choice2 = Choice(
            description=form.choice2.data,
            vote=0, )
        choice3 = Choice(
            description=form.choice3.data,
            vote=0, )
        choice4 = Choice(
            description=form.choice4.data,
            vote=0, )
        poll.choices = [choice1, choice2, choice3, choice4]
        return poll


class Choice(db.Model):
    __tablename__ = "choices"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    vote = db.Column(db.Integer)
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'))
