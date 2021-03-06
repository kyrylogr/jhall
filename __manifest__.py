# -*- coding: utf-8 -*-
{
    'name': "jumping hall",

    'summary': """
        Gym hall management system with schedule, enrollment, abonements.""",

    'description': """
        Gym hall management system with schedule, enrollment, abonements.
    """,

    'author': "Halls",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web_timeline'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'demo/data_initial.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}