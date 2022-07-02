# -*- coding: utf-8 -*-
# By Omar IRAQI.


{
    'name': 'IX Base',
    'version': '1.0',
    'category': 'Education',
    'description': """
The base of all IX apps
===================================================
""",
    'depends': ['web', 'mail', 'attachment_indexation', 'calendar'],
    'data': [
        'security/ix_security.xml',
        'security/ir.model.access.csv',
        'views/course_view.xml',
        'views/discipline_view.xml',
        'views/student_view.xml',
        'views/faculty_view.xml',
        'views/school_view.xml',
        'views/staff_view.xml',
        'views/event_view.xml',
        'views/term_view.xml',
        'views/building_view.xml',
        'views/room_view.xml',
        'views/session_view.xml',
        'views/ix_menu.xml',
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
