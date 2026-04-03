# -*- coding: utf-8 -*-
{
    'name': 'Todo List',
    'version': '18.0.1.0',
    'summary': 'Todo List Management',
    'sequence': 10,
    'description': """
Todo List Management
""",
    'category': 'Productivity',
    'website': 'https://roots.tech',
    'author': 'Natt Srisuwankul',
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'data/todo_tag_data.xml',
        'views/todo_list_views.xml',
        'views/todo_list_menus.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'assets': {},
    'license': 'LGPL-3',
}
