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
from odoo.tests.common import HttpCase
import logging

_logger = logging.getLogger(__name__)


class ComplaintsTests(HttpCase):
    @classmethod
    def setUpClass(cls):
        super(ComplaintsTests, cls).setUpClass()
        cls.main_company_id = cls.env.ref('base.main_company').id
        Users = cls.env['res.users'].with_context(tracking_disable=True)
        cls._user = Users.create({
            'company_id': cls.main_company_id,
            'name': 'Akram Joe',
            'login': 'akram',
            'email': 'akram@example.com',
            'tz': 'Europe/Berlin',
            'groups_id': [(6, 0, cls.env.user.groups_id.ids)],
        })
        # Settings = cls.env['res.config.settings'].with_user(cls._user.id)
        # cls.config = Settings.create({})

    def test_default_settings(self):
        config_settings = self.env['res.config.settings'].create({
            'stage_id': self.env['complaint.stage'].search([('sequence', '=', 0)]).id,
            'assignee': self._user.id
        })
        config_settings.execute()
        self.assertEqual(config_settings.stage_id.sequence, 0)

        _tom_partner = self.env['res.partner'].create({
            'name': 'Tom Scott',
            'email': 'tom@example.com',
            'street': 'Leibnizerstr 41',
        })
        ticket1 = self.env['complaint.ticket'].with_user(self._user).create({
            'name': 'Complaint name 01',
            'partner_id': _tom_partner.id,
        })

        _logger.info(f'test_default_settings, config_settings.assignee: {config_settings.assignee.name}')
        _logger.info(f'test_default_settings, ticket1.user_id: {ticket1.user_id.name}')

        self.assertEqual(config_settings.stage_id.id, ticket1.stage_id.id)
        self.assertEqual(config_settings.assignee.id, ticket1.user_id.id)

    def test_website_complaint_submission(self):
        """ Complaints submission should be available to all users."""
        _data = {
            'name': "Water Leak",
            'partner_name': 'Akram Salem',
            'partner_email': 'akram@example.com',
            'partner_address': 'Leibnizerstraße 41, Stadt',
            'description': 'water leak not stopped since last night',
        }
        self.authenticate(None, None)

        # make sure ticket created and exists
        response = self.url_open('/website/form/complaint.ticket', data=_data)
        ticket = self.env['complaint.ticket'].browse(response.json().get('id'))
        self.assertTrue(ticket.exists())

        # test complaint ticket submission success page
        _complaint_submitted_response = self.url_open('/your-complaint-has-been-submitted')
        self.assertEqual(_complaint_submitted_response.status_code, 200)
