{
    'name': 'IX DMS',
    'version': '11.0.1.0.0',
    'summary': 'IX Document Management System',
    'category': 'Document Management',
    'author': 'Omar IRAQI',
    'maintainer': '',
    'website': '',
    'license': 'LGPL-3',
    'contributors': [
        '',
    ],
    'depends': [
        'ixcatalog',
    ],
    'data': [
        'security/dms_security.xml',
        'security/ir.model.access.csv',
        'views/node_view.xml',
        'views/my_view.xml',
        'views/share_view.xml',
        'views/workspace_view.xml',
        'views/tag_view.xml',
        'views/ixdms_menu.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
