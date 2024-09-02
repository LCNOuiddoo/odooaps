# -*- coding: utf-8 -*-
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enrich_contact = fields.Boolean(related='company_id.enrich_contact', readonly=False,
                                    string='Enrich contact')
    enrich_company = fields.Boolean(related='company_id.enrich_company', readonly=False,
                                    string='Enrich company')
    token_societe_com = fields.Char(related='company_id.token_societe_com', readonly=False,
                                    string='Token societe.com')
