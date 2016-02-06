# -*- coding: utf-8 -*-

from flask import Blueprint
from app.models import Link
from app.utils.view import templated, ensure_resource

bp = Blueprint('share', __name__, template_folder='templates')

@bp.route('/links/<int:id>')
@templated('web/share/link.html')
@ensure_resource(Link)
def get_link(id, link):
    link = Link.query.get_or_404(id)
    return dict(
        link=link,
        tags=[tag for tag in link.tags],
        ads=link.ads,
    )
