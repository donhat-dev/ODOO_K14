{  # type: ignore
    "name": "Training Center",
    "version": "1.0",
    "summary": "A simple Training Center module for Odoo",
    "description": "This module adds a simple Training Center feature to Odoo.",
    "author": "Your Name",
    "category": "Tools",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/training_order_view.xml"
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3"
}