# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def _default_stage_id(self):
        return self.env['complaint.stage'].search([('sequence', '=', 0)], limit=1) \
            or self.env['complaint.stage'].search([], limit=1)

    stage_id = fields.Many2one('complaint.stage', 'Default Complaint Stage',
                               config_parameter='real_estatex_bloopark.stage_id',
                               default=lambda self: self._default_stage_id(),
                               help='Default stage used when creating new complain tickets')

    assignee = fields.Many2one('res.users', 'Default Ticket Assignee',
                               config_parameter='real_estatex_bloopark.assignee',
                               help='Default responsible when a new complaint ticket is created')

    # @api.model
    # def get_values(self):
    #     res = super(ResConfigSettings, self).get_values()
    #     value = self.env['ir.config_parameter'].sudo().get_param('real_estatex_bloopark.stage_id')
    #     res.update(default_stage_id=int(value))
    #     return res
    #
    # @api.model
    # def set_values(self):
    #     res = super(ResConfigSettings, self).set_values()
    #     self.env['ir.config_parameter'].set_param('real_estatex_bloopark.stage_id',
    #                                               str(self.stage_id.id))
    #     return res
