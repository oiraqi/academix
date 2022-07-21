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
from odoo.exceptions import UserError
import string


class Faculty(models.Model):
    _name = 'ix.faculty'
    _inherits = {'res.partner': 'partner_id'}
    _inherit = 'ix.school.owned'
    _description = 'Faculty'
    _order = 'name'

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    user_id = fields.Many2one('res.users', string='User')
    gender = fields.Selection(string='Gender', selection=[('f', 'Female'), ('m', 'Male')], required=True, default='f')
    country_of_origin_id = fields.Many2one(comodel_name='res.country', string='Country of Origin', required=True)
    nationality_id = fields.Many2one(comodel_name='res.country', string='Nationality', required=True)
    hiring_date = fields.Date('Hiring Date')
    discipline_ids = fields.Many2many('ix.discipline', 'ix_faculty_discipline_rel', 'faculty_id', 'discipline_id', 'Disciplines', required=True)
    undergrad_managed_discipline_ids = fields.Many2many('ix.discipline', 'ix_discipline_undergrad_manager_rel', 'manager_id', 'discipline_id', 'Undergraduate Managed Disciplines')
    grad_managed_discipline_ids = fields.Many2many('ix.discipline', 'ix_discipline_grad_manager_rel', 'manager_id', 'discipline_id', 'Graduate Managed Disciplines')    
    room_id = fields.Many2one(comodel_name='ix.room', string='Office')

    @api.model
    def create(self, vals):
        vals['email'] = vals['email'].strip().lower()
        vals['name'] = string.capwords(vals['name'].strip())
        user = self.sudo().env['res.users'].search([('login', '=', vals['email'])])
        if user:
            faculty = self.env['ix.faculty'].search([('user_id', '=', user.id)])
            if faculty:
                raise UserError('Faculty already exists')
            
            vals['partner_id'] = user.partner_id.id
            vals['user_id'] = user.id
            faculty = super(Faculty, self).create(vals)
        else:
            faculty = super(Faculty, self).create(vals)
            user = self.sudo().env['res.users'].create(
                {'login': vals['email'], 'partner_id': faculty.partner_id.id})
            faculty.user_id = user

        user.sudo().groups_id = [(4, self.env.ref('ix.group_faculty').id)]
        return faculty

    @api.onchange('school_id')
    def _onchange_school_id(self):
        for rec in self:
            rec.discipline_ids = False
