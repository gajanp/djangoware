__author__ = 'Val Neekman [neekware.com]'
__version__ = '0.0.1'
__note__ = 'This application simplified navigation menus'

import defaults

if defaults.MENUWARE_AUTOLOAD_TEMPLATE_TAGS:
    from django import template
    application_tags = [
        'menuware.templatetags.header',
        'menuware.templatetags.footer',
        'menuware.templatetags.account',
        'menuware.templatetags.admin',
    ]
    for t in application_tags: template.add_to_builtins(t)
