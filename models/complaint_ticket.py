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


class ComplaintTicket(models.Model):
    _name = 'complaint.ticket'
    _inherit = ['portal.mixin', 'mail.thread.cc', 'mail.activity.mixin']
    _primary_email = 'partner_email'
    _description = 'Complaint ticket'

    def _default_stage_id(self):
        COMPLAINT_STAGE = self.env['complaint.stage']
        config_param_sudo = self.env['ir.config_parameter'].sudo()
        default_stage_id = \
            config_param_sudo.get_param('real_estatex_bloopark.stage_id',
                                        COMPLAINT_STAGE.search([], limit=1))

        return COMPLAINT_STAGE.search([('id', '=', default_stage_id)], limit=1)

    name = fields.Char(string='Subject', required=True, index=True, tracking=True)

    active = fields.Boolean(default=True)
    description = fields.Html(sanitize_attributes=False)

    user_id = fields.Many2one('res.users', string='Assigned to')

    stage_id = fields.Many2one('complaint.stage', string='Stage', index=True,
                               default=lambda self: self._default_stage_id())

    complaint_type_id = fields.Many2one('complaint.type', string='Type', tracking=True)

    partner_email = fields.Char(string='Customer Email', readonly=False)
    partner_name = fields.Char(string='Customer Name', readonly=False)

    partner_id = fields.Many2one('res.partner', string='Customer', tracking=True)