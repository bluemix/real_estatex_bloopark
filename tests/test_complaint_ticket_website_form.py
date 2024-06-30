# import re

from odoo.tests.common import HttpCase
import logging

_logger = logging.getLogger(__name__)


class ComplaintSubmissionWebsite(HttpCase):

    def test_website_complaint_submission(self):
        print('inside test_website_complaint_submission')

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

        # _result = re.search(rb'Your Complaint has being submitted', _complaint_submitted_response.content)
        # print(f'test_website_complaint_submission, _result: {_result}')
