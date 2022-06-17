{
    'name': 'A3 Roster',
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
        'a3catalog'
    ],
    'data': [
        'security/roster_security.xml',
        'security/ir.model.access.csv',        
        'views/section_view.xml',
        'views/enrollment_view.xml',
        'views/room_view.xml',
        'views/reservation_view.xml',
        'views/a3roster_menu.xml',
        'data/standard_events.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
