{  # type: ignore
    "name": "Training Center",
    "version": "1.0",
    "summary": "A simple Training Center module for Odoo",
    "description": "This module adds a simple Training Center feature to Odoo.",
    "author": "Your Name",
    "category": "Tools",
    "depends": ["base", "contacts", "crm", "mail"],
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "views/training_course_view.xml",
        "views/training_order_line_views.xml",
        "views/training_order_options_wizard_views.xml",
        "views/training_order_view.xml",
        "views/templates.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3"
}