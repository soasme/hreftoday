# -*- coding: utf-8 -*-

from dominate import tags
from flask import url_for
from flask_bootstrap.nav import BootstrapRenderer
from flask_nav.elements import View

class TwoSideRenderer(BootstrapRenderer):

    def visit_Navbar(self, node):
        root = super(TwoSideRenderer, self).visit_Navbar(node)

        # hack: add navbar-right block
        collapse = root.children[0].children[1]
        right = tags.ul(_class='nav navbar-nav navbar-right')
        if hasattr(node, 'right_side_items'):
            for item in node.right_side_items:
                right.add(self.visit(item))
        collapse.add(right)

        # hack: logo
        brand = root.children[0].children[0].children[1]
        brand.attributes['class'] = ''
        brand.add(self.visit(node.logo))

        return root

    def visit_Logo(self, node):
        a = tags.a(href=node.get_url())
        a.add(tags.img(src=node.get_image_url()))
        return a

class Logo(View):

    def __init__(self, filename, endpoint, *args, **kwargs):
        super(Logo, self).__init__('', endpoint, *args, **kwargs)
        self.filename = filename

    def get_image_url(self):
        return url_for('static', filename=self.filename)
