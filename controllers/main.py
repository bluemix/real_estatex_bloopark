# -*- coding: utf-8 -*-
##############################################################################
#
#    Author:  Abdulmomen Bsruki (a.bluemix@gmail.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo.http import request
from odoo.addons.website.controllers import form


class WebsiteForm(form.WebsiteForm):

    def _handle_website_form(self, model_name, **kwargs):
        """ overridden to check customer email, and create a new `res.partner` based on it when not found """

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
