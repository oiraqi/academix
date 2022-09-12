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
    'depends': ['ixcrm'],
    'data': [
        'security/ixadmission_security.xml',
        'security/ir.model.access.csv',
        'views/crm_lead_view.xml',
        'views/education_system_view.xml',
        'views/institution_view.xml',
        'views/degree_view.xml',
        'views/ixadmission_menu.xml',
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
