# -*- coding: utf-8 -*-

from flask_nav.elements import View, RawTag

# http://pythonhosted.org/flask-nav/api.html#flask_nav.elements.View
# text, endpoint
NAV_BAR_ITEMS = [
    View('Href Today', 'web.get_topics'),
]
