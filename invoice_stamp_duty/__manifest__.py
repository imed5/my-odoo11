# -*- coding: utf-8 -*-
{
    'name': "Stamp Duty for Invoices",
    'summary': "Add a stamp duty to invoices",
    'description': """
	Allows the option to add/remove a stamp duty to an invoice
    """, 
    'author': "ERPish.com",
    'website': "http://www.erpish.com",
    'category': 'Sales', 
    'version': '11.0.1.2',   
    'depends': ['account','sale'],
    'data': [
        'views/myinvoice.xml',
    ],
    'installable': True,
    'application': True,   
    'auto_install': False,
}
