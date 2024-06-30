from odoo.http import request

from odoo.addons.website.controllers import form

import logging

_logger = logging.getLogger(__name__)


class WebsiteForm(form.WebsiteForm):

    def _handle_website_form(self, model_name, **kwargs):
        """ overridden to check customer email, and create a new `res.partner` based on it when not found """
        _logger.info(f'_handle_website_form, model_name: {model_name}')
        _logger.info(f'_handle_website_form, kwargs: {kwargs}')
        _logger.info(f'_handle_website_form, request.params: {request.params}')

        email = request.params.get('partner_email')
        if email:
            partner = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
            if not partner:
                partner = request.env['res.partner'].sudo().create({
                    'email': email,
                    'name': request.params.get('partner_name', False),
                    'street': request.params.get('partner_address', False),
                })
            request.params['partner_id'] = partner.id

        return super(WebsiteForm, self)._handle_website_form(model_name, **kwargs)
