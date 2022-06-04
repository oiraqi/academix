# -*- coding: utf-8 -*-
# By Omar IRAQI. Courtesy of Galactis


{
    'name': 'AUI Faculty Evaluation -- Evaluation by Administration',
    'version': '1.0',
    'category': 'Hidden',
    'description': """
The Evaluation by Administration module under Faculty Evaluation.
===================================================
""",
    'depends': ['a3_performance_eval'],
    'data': [
        'security/fe_ev_security.xml',
        'security/ir.model.access.csv',
        'views/process_view.xml',
        'views/ts_process_view.xml',
        'views/rp_process_view.xml',
        'views/sd_process_view.xml',
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
