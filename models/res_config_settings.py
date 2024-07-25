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

from odoo import fields, models, _


class ResConfigSettings(models.TransientModel):
    """ overridden to specify the selection of default `stage_id` and default responsible or `assignee` for the
      `complaint.ticket` """
    _inherit = 'res.config.settings'

    def _default_stage_id(self):
        return self.env['complaint.stage'].search([('sequence', '=', 0)], limit=1) \
            or self.env['complaint.stage'].search([], limit=1)

    stage_id = fields.Many2one('complaint.stage', 'Default Complaint Stage',
                               config_parameter='real_estatex.stage_id',
                               default=lambda self: self._default_stage_id(),
                               help='Default stage used when creating new complain tickets')

    assignee = fields.Many2one('res.users', 'Default Ticket Assignee',
                               config_parameter='real_estatex.assignee',
                               help='Default responsible when a new complaint ticket is created')
