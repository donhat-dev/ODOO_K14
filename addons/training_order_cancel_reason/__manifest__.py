# -*- coding: utf-8 -*-
{
    'name': 'Training Order Cancel Reason',
    'version': '1.0',
    'summary': """ Training_order_cancel_reason Summary """,
    'author': '',
    'website': '',
    'category': 'Tools',
    'depends': ['training_center'],
    "data": [
        "security/ir.model.access.csv",
        "wizards/training_order_cancel_wizard.xml",
        "views/training_order_views.xml",
    ],
    
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
