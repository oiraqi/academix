# -*- coding: utf-8 -*-
# By Omar IRAQI.


{
    'name': 'A3 Base',
    'version': '1.0',
    'category': 'Education',
    'description': """
The base of all A3 apps
===================================================
""",
    'depends': ['web', 'mail', 'attachment_indexation'],
    'data': [
        'security/a3_security.xml',
        'security/ir.model.access.csv',
        'views/course_view.xml',
        'views/discipline_view.xml',
        'views/student_view.xml',
        'views/faculty_view.xml',
        'views/school_view.xml',
        'views/staff_view.xml',
        'views/a3_menu.xml',
        'data/schools.xml',
        'data/disciplines.xml',
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
