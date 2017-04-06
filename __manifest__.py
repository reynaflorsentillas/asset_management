# -*- coding: utf-8 -*-
{
    'name': "Asset Management",

    'summary': """
        Asset Management Solutions
    """,
    'description': """
        - Assets
        - Asset Tags
        - Asset States
        - Location of Assets
        - Asset Transactions (Fixed Reader)
        - Security Gate
        - Configure RFID Readers
    """,

    'author': "Capstone Solutions Inc.",
    'website': "http://www.capstone.ph",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Industries',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        'data/ir_sequence_data.xml',
        'data/asset_management_state_data.xml',
        'data/stock_data.xml',
        'security/asset_management_security.xml',
        'security/ir.model.access.csv',
        'views/asset_management_product_view.xml',
        'views/asset_management_view.xml',
        'views/asset_management_transaction_view.xml',
        'views/asset_management_security_gate_view.xml',
        'views/asset_management_reader_view.xml',
        'views/asset_management_menu.xml',
        'views/asset_management.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}