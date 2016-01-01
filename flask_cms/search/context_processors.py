from flask_cms.search.forms import SearchForm


def add_search_form():
    def search_form():
        return SearchForm()
    return dict(search_form=search_form)
