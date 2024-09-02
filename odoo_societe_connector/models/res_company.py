# -*- coding: utf-8 -*-
from odoo import fields, models, api
import logging

_logger = logging.getLogger("Societe.com")

class ResCompany(models.Model):
    _inherit = "res.company"

    enrich_contact = fields.Boolean(string="Enrich contact")
    enrich_company = fields.Boolean(string="Enrich company")
    token_societe_com = fields.Char(string="Token societe.com")
