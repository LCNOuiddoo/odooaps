# -*- coding: utf-8 -*-
{
    'name': "Connecteur Societe.com",
    'summary': """This module allow to connect Odoo with societe.com""",
    'description': """
        This module enables integration between Odoo and Societe.com, allowing seamless synchronization of company and contact information.
    """,
    'author': "Ouiddoo",
    'website': "https://www.ouiddoo.fr/",
    "version": "17.0.0.1.0",
    'depends': ['contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/res_company_views.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
    'auto_install': False,
}
