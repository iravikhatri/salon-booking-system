# -*- coding: utf-8 -*-
{
    'name': "Appointment Booking",

'summary': """
        
    """,

    'description': """
       
    """,

    'author': "TechNeith",

    'website': "https://www.techneith.com",

    'category': 'Uncategorized',

	'images': ['static/description/images/banner.png'],

    'price' : 299,

    'currency' : 'EUR',

    'version': '1.0',

    "license" : 'LGPL-3',


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
