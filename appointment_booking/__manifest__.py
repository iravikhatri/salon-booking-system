# -*- coding: utf-8 -*-
{
    'name': "Appointment Booking",

    'summary': """
        Shomodules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "TechNeith",
    'website': "https://www.techneith.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'sale_management', 'website_sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
		'views/calendar.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
