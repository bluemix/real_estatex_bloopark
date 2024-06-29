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
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class ComplaintTicket(models.Model):
    _name = 'complaint.ticket'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _primary_email = 'partner_email'
    _description = 'Complaint ticket'

    def _default_stage_id(self):
        COMPLAINT_STAGE = self.env['complaint.stage']
        config_param_sudo = self.env['ir.config_parameter'].sudo()
        default_id = \
            config_param_sudo.get_param('real_estatex_bloopark.stage_id', False)
        if not default_id:
            raise UserError(_("Please assign a default stage from the module settings"))
        return COMPLAINT_STAGE.search([('id', '=', default_id)], limit=1)

    def _default_assignee_id(self):
        RES_USERS = self.env['res.users']
        config_param_sudo = self.env['ir.config_parameter'].sudo()
        default_id = \
            config_param_sudo.get_param('real_estatex_bloopark.assignee', False)
        if not default_id:
            raise UserError(_("Please assign a default assignee from the module settings"))
        return RES_USERS.search([('id', '=', default_id)], limit=1)

    name = fields.Char(string='Subject', required=True, index=True, tracking=True)

    active = fields.Boolean(default=True)
    description = fields.Html(sanitize_attributes=False)

    user_id = fields.Many2one('res.users', string='Assigned to',
                              default=lambda self: self._default_assignee_id())

    stage_id = fields.Many2one('complaint.stage', string='Stage', index=True,
                               default=lambda self: self._default_stage_id())

    complaint_type_id = fields.Many2one('complaint.type', string='Type', tracking=True)

    partner_email = fields.Char(string='Customer Email', readonly=False)
    partner_name = fields.Char(string='Customer Name', readonly=False)
    partner_address = fields.Char(string='Customer Address')

    partner_id = fields.Many2one('res.partner', string='Customer',
                                 store=True,
                                 compute='_compute_partner_id', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        _logger.info(f'create, vals_list: {vals_list}')
        _logger.info(f'create, self.env.context: {self.env.context}')

        _tickets = super(ComplaintTicket, self).create(vals_list)
        for _ticket in _tickets:
            _ticket.send_email()
        return _tickets

    @api.onchange('stage_id')
    def send_email(self):
        """ will send an email based on the stage of the ticket """
        for rec in self:
            if rec.stage_id.sequence == 0:
                email_template_id = self.env['ir.model.data']._xmlid_to_res_id(
                    'real_estatex_bloopark.mail_template_complaint_created', raise_if_not_found=False
                )
                rec.with_context(force_send=True).message_post_with_template(email_template_id)
            elif rec.stage_id.sequence == 4 or rec.stage_id.sequence == 3:
                email_template_id = self.env['ir.model.data']._xmlid_to_res_id(
                    'real_estatex_bloopark.mail_template_complaint_finished', raise_if_not_found=False
                )
                rec.with_context(force_send=True).message_post_with_template(email_template_id)

    @api.depends('partner_email')
    def _compute_partner_id(self):
        for rec in self:
            _partner = self.env['res.partner'].sudo().search([('email', '=', rec.partner_email)], limit=1)
            rec.partner_id = _partner or rec.partner_id

