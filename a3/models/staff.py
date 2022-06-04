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

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import string


class Staff(models.Model):
    _name = 'a3.staff'
    _inherits = {'res.partner': 'partner_id'}

    school_ids = fields.Many2many('a3.school', string='Schools')
    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True)
    user_id = fields.Many2one('res.users', string='User')
    is_setup = fields.Boolean('Setup', default=False)
    is_coordinator = fields.Boolean('Coordinator', default=False)
    is_dean = fields.Boolean('Dean', default=False)
    is_vpaa = fields.Boolean('VPAA', default=False)
    is_president = fields.Boolean('President', default=False)

    @api.model
    def create(self, vals):
        vals['email'] = vals['email'].strip().lower()
        vals['name'] = string.capwords(vals['name'].strip())
        user = self.sudo().env['res.users'].search(
            [('login', '=', vals['email'])])
        if user:
            staff = self.env['a3.staff'].search([('user_id', '=', user.id)])
            if staff:
                raise UserError('Faculty already exists')

            vals['partner_id'] = user.partner_id.id
            vals['user_id'] = user.id
            staff = super(Staff, self).create(vals)
        else:
            staff = super(Staff, self).create(vals)
            user = self.sudo().env['res.users'].create(
                {'login': vals['email'], 'partner_id': staff.partner_id.id})
            staff.user_id = user

        group_ids = []
        # group_ids.append(self.env.ref('a3.group_faculty').id)

        if staff.is_setup:
            group_ids.append((4, self.env.ref('a3.group_setup').id))
        if staff.is_coordinator:
            group_ids.append((4, self.env.ref('a3.group_coordinator').id))
        if staff.is_dean:
            group_ids.append((4, self.env.ref('a3.group_dean').id))
        if staff.is_vpaa:
            group_ids.append((4, self.env.ref('a3.group_vpaa').id))
        if staff.is_president:
            group_ids.append((4, self.env.ref('a3.group_president').id))

        if len(group_ids) > 0:
            user.sudo().groups_id = group_ids
        
        return staff

    def write(self, vals):
        if 'email' in vals:
            vals['email'] = vals['email'].strip().lower()
        for staff in self:
            group_ids = []
            if staff.is_setup:
                group_ids.append(self.env.ref('a3.group_setup').id)
            if staff.is_coordinator:
                group_ids.append(self.env.ref('a3.group_coordinator').id)
            if staff.is_dean:
                group_ids.append(self.env.ref('a3.group_dean').id)
            if staff.is_vpaa:
                group_ids.append(self.env.ref('a3.group_vpaa').id)
            if staff.is_president:
                group_ids.append(self.env.ref('a3.group_president').id)

            staff.user_id.sudo().groups_id = [(6, 0, group_ids)]

        return super(Staff, self).write(vals)
