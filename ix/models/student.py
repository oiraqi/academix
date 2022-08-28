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


class Student(models.Model):
    _name = 'ix.student'
    _inherit = ['ix.partnered', 'ix.school.owned', 'mail.thread']
    _description = 'Student'
    _order = 'name'
    _sql_constraints = [('sid_ukey', 'unique(sid)', 'Student ID already exists')]

    @api.model
    def create(self, vals):
        vals['email'] = vals['email'].strip().lower()
        vals['name'] = string.capwords(vals['name'].strip())
        lastname_firstname = vals['name'].split(', ')
        if len(lastname_firstname) != 2:
            raise UserError('Student name shall be formatted as: Lastname, Firstname')
        
        if 'lastname' not in vals:
            vals['lastname'] = lastname_firstname[0]
        if 'firstname' not in vals:
            vals['firstname'] = lastname_firstname[1]
        user = self.sudo().env['res.users'].search([('login', '=', vals['email'])])
        if user:
            student = self.env['ix.student'].search([('user_id', '=', user.id)])
            if student:
                raise UserError('Student already exists')
            
            vals['partner_id'] = user.partner_id.id
            vals['user_id'] = user.id
            student = super(Student, self).create(vals)
        else:
            student = super(Student, self).create(vals)
            user = self.sudo().env['res.users'].create(
                {'login': vals['email'], 'partner_id': student.partner_id.id})
            student.user_id = user

        user.sudo().groups_id = [(4, self.env.ref('ix.group_student').id)]
        return student

    sid = fields.Char(string='ID', required=True)
    attendance_mode = fields.Selection(string='Attendance Mode', selection=[('f2f', 'Face To Face'), ('online', 'Online'),], default='f2f', required=True, tracking=True)
    max_ncourses = fields.Integer(string='Max Number of Courses / Semester', default=6, required=True, tracking=True)
    max_ncredits = fields.Integer(string='Max Number of Credits / Semester', default=18, required=True, tracking=True)
