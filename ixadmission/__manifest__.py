# -*- coding: utf-8 -*-
# By Omar IRAQI.


{
    'name': 'IX Admission',
    'version': '1.0',
    'category': 'Education',
    'description': """
The IX Admission Module
===================================================
""",
    'depends': ['ix'],
    'data': [
        'security/ix_security.xml',
        'security/ir.model.access.csv',
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
