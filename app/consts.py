# -*- coding: utf-8 -*-

from flask_nav.elements import View, Subgroup, Navbar
from flask_login import current_user
from app.utils.navbar_renderer import Logo

def get_navbar():
    navbar = Navbar('', *[
        View('Href Today', 'dashboard.get_links'),
    ])
    navbar.logo = Logo('images/logo.png', 'web.get_topics')
    if current_user.is_anonymous:
        navbar.right_side_items = [View('Login', 'user.login')]
    else:
        navbar.right_side_items = [
            Subgroup(
                'Account',
                View('Change Password', 'user.change_password'),
                View('Logout', 'user.logout'),
            )
        ]
    return navbar
