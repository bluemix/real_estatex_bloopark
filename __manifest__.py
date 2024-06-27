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
{
    'name': "RealEstateX",
    'version': '16.0.0.9.0',
    'category': 'Extra Tools',
    'summary': """Real Estate Complaints Management""",
    'description': """RealEstateX will provide a form on their website for tenants to submit complaints about their
              rented flats. These complaints will then be classified and dealt with by RealEstateX’s employees.""",
    'author': 'Abdulmomen Bsruki',
    'maintainer': 'Abdulmomen Bsruki',
    'website': 'bluemix.me',
    'depends': ['website', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/complaint_template.xml',
        'views/complaint_submitted_template.xml',
        'views/complaint_ticket_views.xml',
        'views/complaint_stage_views.xml',
        'views/complaint_type_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True
}
