# -*- coding: utf-8 -*-
# By Omar IRAQI. Courtesy of Galactis


{
    'name': 'IX Performance',
    'version': '1.0',
    'category': 'Hidden',
    'description': """
The Faculty Performance Management App.
===================================================
""",
    'depends': ['ix'],
    'data': [
        'security/performance_security.xml',
        'security/ir.model.access.csv',
        'views/faculty_view.xml',
        'views/srank_view.xml',
        'views/staff_view.xml',
        'views/process_view.xml',
        'views/performance_menu.xml',
        'data/sranks.xml'
        
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
