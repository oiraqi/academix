# -*- coding: utf-8 -*-
# By Omar IRAQI. Courtesy of Galactis


{
    'name': 'A3 Performance -- SD',
    'version': '1.0',
    'category': 'Hidden',
    'description': """
The Service and Development module under Performance Management.
===================================================
""",
    'depends': ['a3performance'],
    'data': [
        #'security/performance_eval_security.xml',
        'security/ir.model.access.csv',
        'views/committee_activity_view.xml',
        'views/process_view.xml',
        'views/performance_sd_menu.xml',
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
