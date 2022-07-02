{
    'name': 'IX Research',
    'version': '1.0',
    'summary': 'Manages and organizes rsearch production',
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
        'security/ir.model.access.csv',
        'views/journal_view.xml',
        'views/publisher_view.xml',
        'views/article_view.xml',
        'views/book_view.xml',
        'views/presentation_view.xml',
        'views/paper_view.xml',
        'views/activity_view.xml',
        'views/school_view.xml',
        'views/research_menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}