# -*- coding: utf-8 -*-
# By Omar IRAQI. Courtesy of Galactis


{
    'name': 'A3 Performance -- Evaluation',
    'version': '1.0',
    'category': 'Hidden',
    'description': """
The Evaluation module under Performance Management.
===================================================
""",
    'depends': ['a3performance'],
    'data': [
        'security/performance_eval_security.xml',
        'security/ir.model.access.csv',
        'views/process_view.xml',
        'views/ts_process_view.xml',
        'views/rp_process_view.xml',
        'views/sd_process_view.xml',
        'views/performance_eval_menu.xml',
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
