# -*- coding: utf-8 -*-
{
    'name': "Theme Vivre",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "TechNeith",
    'website': "https://www.techneith.com",

    'category': 'theme',
    'version': '0.1',

    'depends': ['base', 'website_sale', 'appointment_booking'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/snippets.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],
}
