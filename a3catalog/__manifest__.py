{
    'name': 'A3 Catalog',
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
        'a3',
    ],
    'data': [
        'security/ir.model.access.csv',
        #'security/catalog_security.xml',
        'views/course_view.xml',
        'views/program_view.xml',
        'views/component_view.xml',
        'views/school_view.xml',
        'views/catalog_menu.xml',
        'data/ucourses.xml',
        'data/corequisites.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
