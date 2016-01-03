from itertools import izip_longest

from flask import url_for, request

from flask_cms.page.models import Page
from flask.ext.security import current_user


def get_breadcrumbs(page, breadcrumbs=None):
    if not breadcrumbs:
        breadcrumbs = []

    breadcrumbs.append(page.slug)
    if page.parent is None:
        breadcrumbs.reverse()
        return breadcrumbs
    breadcrumbs = get_breadcrumbs(page.parent, breadcrumbs)
    return breadcrumbs


def create_breadcrumbs_snippet():
    def add_breadcrumbs_snippet(page):
        snippet = ''
        breadcrumbs = get_breadcrumbs(page)
        if not breadcrumbs:
            return snippet
        snippet = "<ul class='breadcrumb'>"
        for breadcrumb in breadcrumbs:
            snippet += '<li><a href="{url}">{camelized_slug}</a></li>'. \
                format(url=url_for('page.show', slug=breadcrumb),
                       camelized_slug=breadcrumb.title())
        snippet += '</ul>'
        return snippet

    return dict(add_breadcrumbs_snippet=add_breadcrumbs_snippet)


def add_grouper():
    def grouper(iterable, n, fillvalue=None):
        "Collect data into fixed-length chunks or blocks"
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
        args = [iter(iterable)] * n
        return izip_longest(fillvalue=fillvalue, *args)

    return dict(grouper=grouper)


def add_navbar():
    def navbar():
        snippet = '<ul class="nav navbar-nav">'
        if current_user.is_authenticated:
            pages_to_show = Page.query.filter_by(publish=True, show_in_nav=True, level=0)
        else:
            pages_to_show = Page.query.filter_by(publish=True, show_in_nav=True, level=0, login_required=False)

        for page in pages_to_show:
            if page.children.all():
                snippet += '<li class="dropdown">'
                snippet += '''<a href="#" class="dropdown-toggle"
                data-toggle="dropdown" role="button"
                aria-haspopup="true" aria-expanded="false">
                {title}</a>'''. \
                    format(title=page.title.title())
                snippet += '<ul class="dropdown-menu">'
                for child in page.children:
                    snippet += '<li><a href="{url}">{title}</a></li>'. \
                        format(url=url_for("page.show", slug=child.slug),
                               title=child.title.title(), )
                snippet += '</ul></li>'
            else:
                css_class = ""
                if request.path.split("/")[-1] == page.slug:
                    css_class = 'class="active"'
                snippet += '<li {css_class}><a href="{url}">{title}</a></li>'. \
                    format(css_class=css_class,
                           url=url_for("page.show", slug=page.slug),
                           title=page.title.title())
        snippet += '</ul>'
        return snippet

    return dict(navbar=navbar)
