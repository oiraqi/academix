{
    'name': 'IX CRM',
    'version': '1.0',
    'summary': 'An Integrated CRM',
    'category': 'Education',
    'author': 'Omar IRAQI',
    'maintainer': '',
    'website': '',
    'license': 'LGPL-3',
    'contributors': [
        '',
    ],
    'depends': [
        'ixcatalog',
        'crm',
    ],
    'data': [
        'security/ixcrm_security.xml',
        'security/ir.model.access.csv',
        'views/crm_lead_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
