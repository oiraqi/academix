# -*- coding: utf-8 -*-
###############################################################################
#
#    Al Akhawayn University in Ifrane -- AUI
#    Copyright (C) 2022-TODAY AUI(<http://www.aui.ma>).
#
#    Author: Omar Iraqi Houssaini | https://github.com/oiraqi
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import models, fields


class Staff(models.Model):
    _inherit = 'a3.staff'

    is_committee_member = fields.Boolean('EC Member', default=False)
    is_committee_chair = fields.Boolean('EC Chair', default=False)

    def write(self, vals):
        for staff in self:
            if 'is_committee_chair' in vals and vals['is_committee_chair']:
                staff.user_id.sudo().groups_id = (4, self.enf.ref('a3performance.group_committee_chair').id)
            elif 'is_committee_member' in vals and  vals['is_committee_member']:
                staff.user_id.sudo().groups_id = (4, self.enf.ref('a3performance.group_committee_member').id)
        
        return super(Staff, self).write(vals)
