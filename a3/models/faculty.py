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


class Faculty(models.Model):
    _name = 'a3.faculty'
    _inherits = {'res.partner': 'partner_id'}
    _inherit = 'a3.school.owned'
    _description = 'Faculty'

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    user_id = fields.Many2one('res.users', string='User')
    hiring_date = fields.Date('Hiring Date')
    course_ids = fields.Many2many('a3.course', 'a3_course_faculty_rel', 'instructor_id', 'course_id', string='Taught Courses')

    @api.model
    def create(self, vals):
        vals['email'] = vals['email'].strip().lower()
        vals['name'] = string.capwords(vals['name'].strip())
        user = self.sudo().env['res.users'].search([('login', '=', vals['email'])])
        if user:
            faculty = self.env['a3.faculty'].search([('user_id', '=', user.id)])
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

        user.sudo().groups_id = [(4, self.env.ref('a3.group_faculty').id)]
        return faculty
