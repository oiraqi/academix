# -*- coding: utf-8 -*-
# By Omar IRAQI.


{
    'name': 'A3 Projects',
    'version': '1.0',
    'category': 'Education',
    'description': """
Student Capstones, Internships, Combined, Master Projects and Theses.
===================================================
""",
    'depends': ['ixroster'],
    'data': [
        'security/capint_security.xml',
        'security/ir.model.access.csv',
        'views/project_view.xml',
        'views/evaluation_view.xml',
        'views/capint_menu.xml',
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
