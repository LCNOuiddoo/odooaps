# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
import logging
import datetime
from odoo.exceptions import UserError


_logger = logging.getLogger("Societe.com")
from .. import societeapi



class ResPartner(models.Model):
    _inherit = "res.partner"

    siret = fields.Char(string="Siret")
    registration_date = fields.Date(string="Date registration")
    create_date_insee = fields.Date(string="Create date INSEE")
    closing_date = fields.Date(string="Closing date")
    code_naf = fields.Char(string="Code NAF")
    capital_company = fields.Float(string="Capital company")
    ref_societe_com = fields.Char(string="Ref societe.com")
    already_enriched = fields.Boolean(string="Already Enriched", default=False)


    def convert_date_format(self, date_str):
        """
           This method parses a date string in the format 'YYYYMMDD' into a datetime object
           and then formats it as a string suitable for Odoo's date fields.

           Args:
               date_str (str): The date string in 'YYYYMMDD' format.

           Returns:
               str: The formatted date string in 'YYYY-MM-DD' format. Returns an empty string if date_str is None.
        """
        odoo_date_str = ""
        if date_str:
            # Parse the date string into a datetime object
            date_obj = datetime.datetime.strptime(date_str, "%Y%m%d")

            # Format the datetime object as an Odoo date string
            odoo_date_str = date_obj.strftime("%Y-%m-%d")
        return odoo_date_str


    def get_country(self, country_name):
        """
            This method searches for a country record where the name partially matches
            the provided country_name.

            Args:
                country_name (str): The name of the country to search for.

            Returns:
                res.country: The country record that matches the search criteria. Returns an empty recordset if no match is found.
        """
        ResCountry = self.env['res.country']
        if country_name:
            return ResCountry.search([('name', 'like', country_name)], limit=1)
        return ResCountry


    def get_partner_title(self, title_name):
        """
            This method maps common abbreviations to their full title equivalents
            and then searches for a partner title record where the shortcut matches.

            Args:
                title_name (str): The title abbreviation or name to search for. Common abbreviations are mapped (e.g., 'M' to 'M.', 'MME' to 'Mme').

            Returns:
                res.partner.title: The partner title record that matches the search criteria. Returns an empty recordset if no match is found.
        """
        ResPartnerTitle = self.env['res.partner.title']
        title_mapping = {'M': 'M.', 'MME': 'Mme'}
        if title_name:
            title_name = title_mapping.get(title_name, title_name)
            title = ResPartnerTitle.search([('shortcut', '=', title_name)], limit=1)
            return title
        return ResPartnerTitle

    def _prepare_company_partner(self, infolegales):
        """
            This method extracts relevant fields from the provided infolegales dictionary
            and formats them into a structure suitable for Odoo's res.partner model.

            Args:
                infolegales (dict): A dictionary containing legal information about the company.

            Returns:
                dict: A dictionary containing the fields and values to update or create a company partner record.
        """
        correct_name = infolegales.get('denoinsee') or infolegales.get('denorcs') or ''
        current_name = self.display_name or self.name
        if current_name.lower().strip() != correct_name.lower().strip():
            display_name = f"{current_name} ({correct_name})"
        else:
            display_name = correct_name
        return {
            "siret": infolegales.get('siretsiege') or '',
            "display_name": display_name,
            "name": display_name,
            "vat": infolegales.get('numtva') or '',
            "company_registry": infolegales.get('rcs') or '',
            "registration_date": self.convert_date_format(infolegales.get('datecrearcs')) or '',
            "create_date_insee": self.convert_date_format(infolegales.get('datecreainsee')) or '',
            "code_naf": infolegales.get('nafinsee') or '' + '-' + infolegales.get('naflibinsee') or '',
            "street": infolegales.get('voieadressageinsee') or '',
            "zip": infolegales.get('codepostalinsee') or '',
            "city": infolegales.get('villeinsee') or '',
            "country_id": self.get_country(infolegales.get('paysinsee')).id,
            "capital_company": infolegales.get('capital') and float(infolegales.get('capital').replace(',', '.')) or 0,
            # "closing_date": self.convert_date_format(infolegales.get('datebilan')) or '',
        }

    def update_company_fields(self, resp):
        """
            This method processes the API response and updates the company partner record
            with the data extracted. Raises an exception if the response is not successful.

            Args:
                resp (requests.Response): The HTTP response object from the API request.

            Raises:
                UserError: If the response status code is not 200.
        """
        if resp and resp.status_code == 200:
            self.write(self._prepare_company_partner(next(iter(resp.json().values()))))
        else:
            raise UserError(_("Error code %s: something went wrong to update company") %(resp.status_code))
        return True

    def _prepare_contact_partner(self, dirigeant):
        """
            This method extracts relevant fields from the provided dirigeant dictionary
            and formats them into a structure suitable for Odoo's res.partner model.

            Args:
                dirigeant (dict): A dictionary containing information about an executive.

            Returns:
                dict: A dictionary containing the fields and values to update or create a contact partner record.
        """
        if not dirigeant.get('titre') or (not dirigeant.get('prenompp') and not dirigeant.get('nompp')):
            return {}
        return {
            "parent_id": self.id,
            "type": 'contact',
            "is_company":False,
            "function": dirigeant.get('titre') or '',
            "title":  self.get_partner_title(dirigeant.get('civpp')).id,
            "ref_societe_com": dirigeant.get('id_dir_pp') or  dirigeant.get('id_dir_pm'),
            "name": "%s %s" % (dirigeant.get('prenompp'), dirigeant.get('nompp'))
        }

    def update_contact_fields(self, resp):
        """
            This method processes the API response and updates or creates contact partner records
            based on the data for executives. Raises an exception if the response is not successful.

            Args:
                resp (requests.Response): The HTTP response object from the API request.

            Raises:
                UserError: If the response status code is not 200.
        """
        if resp and resp.status_code == 200:
            dirigeants = next(iter(resp.json().values())).get('dirigeants')
            for dirigeant in dirigeants:
                partner_id = self.search([
                    ('ref_societe_com','=', dirigeant.get('id_dir_pp') or dirigeant.get('id_dir_pm'))
                ], limit=1)
                vals = self._prepare_contact_partner(dirigeant)
                if vals:
                    if partner_id:
                        partner_id.write(vals)
                    else:
                        self.create(vals)
        else:
            raise UserError(_("Error code %s: something went wrong to update contact of this company") %(resp.status_code))
        return True

    def update_record(self):
        """
            This method retrieves data from the Societe.com API and updates both company and contact
            records if the necessary conditions are met. It handles the API responses and logs any errors.

            Raises:
                UserError: If the API token is missing or if neither VAT nor SIRET is provided.
        """
        if self.env.company.token_societe_com and (self.vat or self.siret):
            societea_pi = societeapi.api.API(token=self.env.company.token_societe_com)
            if self.env.company.enrich_company:
                resp = societea_pi.get("/entreprise/%s/infoslegales" %(self.siret or self.vat))
                _logger.info("/entreprise/infoslegales : %s", resp)
                try:
                    self.update_company_fields(resp)
                    self.env.cr.commit()
                except Exception as error:
                    _logger.info("Something went wrong while %s"%(str(error)))
            if self.env.company.enrich_contact:
                resp = societea_pi.get("/entreprise/%s/dirigeants" % (self.siret or self.vat))
                _logger.info("/entreprise/dirigeants : %s", resp)
                try:
                    self.update_contact_fields(resp)
                    self.env.cr.commit()
                except Exception as error:
                    _logger.info("Something went wrong while %s" % (str(error)))

        elif not self.env.company.token_societe_com:
            raise UserError(_("Please check the societe.com token in company profile"))
        else:
            raise UserError(_("please enter the VAT or siret number to start the search"))





