from flask import request, render_template, flash, url_for
from flask.views import MethodView
from sqlalchemy import text, or_
from werkzeug.exceptions import abort
from werkzeug.utils import import_string, redirect


class SearchView(MethodView):
    def _get_search_results(self, q):
        from flask_cms.app import app

        results = {}
        searchable_models = app.config.get("SEARCHABLE_MODELS", [])
        for model in searchable_models:
            model_string = model[0]
            model_class = import_string(model_string)

            # Only get these columns from db
            columns_to_select = model[2]
            entities = [import_string("{}.{}".format(model_string, column))
                        for column in columns_to_select]

            # build search condition
            searchable_columns = model[1]
            column_objs = [import_string("{}.{}".format(model_string, column))
                           for column in searchable_columns]
            search_condition = [obj.like("%{}%".format(q))
                                for obj in column_objs]

            # query model with entities for search condition
            model_results = (model_class.query.
                             with_entities(*entities).
                             filter(or_(*search_condition)).
                             params(q=q).all())
            if model_results:
                results[model_class.__tablename__] = model_results
        return results

    def get(self):
        q = request.args.get("q", None, type=str)
        if not q or not q.strip():
            flash("Keyword cannot be empty", "error")
            return redirect(url_for('core.index'))

        q = q.strip()
        results = self._get_search_results(q)
        return render_template("search_results.html", results=results)
