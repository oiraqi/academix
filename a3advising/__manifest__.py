{
    'name': 'A3 Advising',
    'version': '1.0',
    'summary': 'Includes a Degree Planner for Students',
    'category': 'Education',
    'author': 'Omar IRAQI',
    'maintainer': 'Omar IRAQI',
    'website': '',
    'license': '',
    'contributors': [
        '',
    ],
    'depends': [
        'web', 'a3catalog',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/planned_course_view.xml',
        'views/degree_plan_view.xml',
        'views/advising_menu.xml',
        'views/student_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/a3advising/static/src/js/raphael.min.js',
            '/a3advising/static/src/js/dracula.min.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}

