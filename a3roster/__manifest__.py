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
        'a3catalog', 'calendar'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/roster_security.xml',
        'views/section_view.xml',
        'views/roster_menu.xml',
        'data/standard_events.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
