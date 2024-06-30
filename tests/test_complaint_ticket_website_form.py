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


class ComplaintSubmissionWebsite(HttpCase):

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
