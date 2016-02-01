# -*- coding: utf-8 -*-

from dominate import tags
from flask_nav.renderers import SimpleRenderer

class Renderer(SimpleRenderer):

    def visit_RawTag(self, node):
        return tag.span(node.content, _class='nav-rawtag')
