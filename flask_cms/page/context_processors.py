from itertools import izip_longest
from flask import url_for


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
            snippet += '<li><a href="{url}">{camelized_slug}</a></li>'.\
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
