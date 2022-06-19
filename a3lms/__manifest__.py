{
    'name': 'A3 LMS',
    'version': '1.0',
    'summary': 'An Integrated LMS',
    'category': 'Education',
    'author': 'Omar IRAQI',
    'maintainer': '',
    'website': '',
    'license': '',
    'contributors': [
        '',
    ],
    'depends': [
        'a3roster',
    ],
    'data': [
        'security/lms_security.xml',
        'security/ir.model.access.csv',
        'data/assessment_techniques.xml',
        "views/assessment_technique_view.xml",
        'views/lms_course_view.xml',
        'views/course_view.xml',
        'views/lms_menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
