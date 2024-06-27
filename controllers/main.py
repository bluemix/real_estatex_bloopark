from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect

from odoo import http, _
from odoo.http import request
from odoo.osv import expression

from odoo.addons.website.controllers import form

import logging

_logger = logging.getLogger(__name__)


class WebsiteForm(form.WebsiteForm):

    def _handle_website_form(self, model_name, **kwargs):
        _logger.info(f'_handle_website_form, model_name: {model_name}')
        _logger.info(f'_handle_website_form, kwargs: {kwargs}')
        _logger.info(f'_handle_website_form, request.params: {request.params}')

        # email = request.params.get('partner_email')
        # if email:
        #     if request.env.user.email == email:
        #         partner = request.env.user.partner_id
        #     else:
        #         partner = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
        #     if not partner:
        #         partner = request.env['res.partner'].sudo().create({
        #             'email': email,
        #             'name': request.params.get('partner_name', False),
        #             'lang': request.lang.code,
        #         })
        #     request.params['partner_id'] = partner.id

        return super(WebsiteForm, self)._handle_website_form(model_name, **kwargs)
