# -*- coding: utf-8 -*-
# By Omar IRAQI. Courtesy of Galactis


{
    'name': 'A3 Performance -- RP',
    'version': '1.0',
    'category': 'Hidden',
    'description': """
The Research and Publication module under Performance Management.
===================================================
""",
    'depends': ['a3performance', 'a3research'],
    'data': [
        #'security/fe_rp_security.xml',
        'security/ir.model.access.csv',
        'views/activity_view.xml',
        'views/process_view.xml',
        'views/performance_rp_menu.xml'
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
