{
    'name': 'IX Advising',
    'version': '1.0',
    'summary': 'Includes a Degree Planner for Students',
    'category': 'Education',
    'author': 'Omar IRAQI',
    'maintainer': 'Omar IRAQI',
    'website': '',
    'license': 'LGPL-3',
    'contributors': [
        '',
    ],
    'depends': [
        'ixroster',
    ],
    'data': [
        'security/advising_security.xml',
        'security/ir.model.access.csv',
        'views/planned_course_view.xml',
        'views/degree_plan_view.xml',
        'views/advising_menu.xml',
        'views/student_view.xml',
        'views/section_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/ixadvising/static/src/js/raphael.min.js',
            '/ixadvising/static/src/js/dracula.min.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}

