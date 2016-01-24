# -*- coding: utf-8 -*-
__all__ = ['amazon']

from flask import _app_ctx_stack as stack, current_app
from werkzeug.local import LocalProxy
from amazon.api import AmazonAPI

class API(AmazonAPI):

    def get_detail_page_url(self, product):
        return product._safe_get_element_text('DetailPageURL')

def _get_current_amazon():
    amazon = getattr(stack.top, 'amazon', None)
    if amazon:
        return amazon
    _load_current_amazon()
    return getattr(stack.top, 'amazon', None)


def _load_current_amazon():
    stack.top.amazon = API(
        current_app.config.get('AMAZON_ACCESS_KEY'),
        current_app.config.get('AMAZON_SECRET_KEY'),
        current_app.config.get('AMAZON_ASSOC_TAG'),
    )


amazon = LocalProxy(_get_current_amazon)
