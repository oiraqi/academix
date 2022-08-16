# -*- coding: utf-8 -*-
# By Omar IRAQI. Courtesy of Galactis


{
    'name': 'IX Performance -- TS',
    'version': '1.0',
    'category': 'Hidden',
    'description': """
The Teaching and Supervision module under Performance Management.
===================================================
""",
    'depends': ['ixperformance', 'ixroster'],
    'data': [
        #'security/performance_ts_security.xml',
        'security/ir.model.access.csv',
        'views/student_evaluation_view.xml',
        'views/action_view.xml',
        'views/supervision_view.xml',
        'views/process_view.xml',
        'views/performance_ts_menu.xml',
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
