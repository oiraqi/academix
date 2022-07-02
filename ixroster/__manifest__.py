{
    'name': 'IX Roster',
    'version': '1.0',
    'summary': 'Roster Manager',
    'category': 'Education',
    'author': 'Omar IRAQI',
    'maintainer': 'Omar IRAQI',
    'website': '',
    'license': 'LGPL-3',
    'contributors': [
        '',
    ],
    'depends': [
        'ixcatalog'
    ],
    'data': [
        'security/roster_security.xml',
        'security/ir.model.access.csv',
        'views/section_view.xml',
        'views/enrollment_view.xml',
        'views/room_view.xml',
        'views/reservation_view.xml',
        'views/faculty_view.xml',
        'views/student_view.xml',
        'views/roster_menu.xml',
        'data/standard_events.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
