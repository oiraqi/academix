{
    'name': 'IX Catalog',
    'version': '1.0',
    'summary': 'Course and Program Catalog',
    'category': 'Education',
    'author': 'Omar IRAQI',
    'maintainer': 'Omar IRAQI',
    'website': '',
    'license': 'LGPL-3',
    'contributors': [
        '',
    ],
    'depends': [
        'ix',
    ],
    'data': [
        'security/catalog_security.xml',
        'security/ir.model.access.csv',        
        'views/course_view.xml',
        'views/program_view.xml',
        'views/component_view.xml',
        'views/school_view.xml',
        'views/student_view.xml',
        'views/catalog_menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}