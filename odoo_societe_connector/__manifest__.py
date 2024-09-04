# -*- coding: utf-8 -*-
{
    'name': "Connecteur Societe.com",
    'summary': """Ce module permet de connecter Odoo à Societe.com.""",
    'description': """
        Ce module permet l'intégration entre Odoo et Societe.com, offrant une synchronisation fluide des informations d'entreprise et de contacts.
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
    'price': 19.90,
    'currency': 'EUR',

}
