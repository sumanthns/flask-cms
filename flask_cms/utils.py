from sqlalchemy import and_
from sqlalchemy.orm import exc
from werkzeug.exceptions import abort
from wtforms import TextAreaField
from wtforms.widgets import TextArea


def get_object_or_404(model, *criterion):
    try:
        return model.query.filter(and_(*criterion)).one()
    except exc.NoResultFound, exc.MultipleResultsFound:
        abort(404)

class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()
