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


class ResUsers(models.Model):
    _inherit = 'res.users'

    school_ids = fields.One2many('a3.school', compute='_school_ids')
    student_id = fields.Many2one(comodel_name='a3.student', compute='_student')
    faculty_id = fields.Many2one(comodel_name='a3.faculty', compute='_faculty')
    staff_id = fields.Many2one(comodel_name='a3.staff', compute='_staff')


    def _student(self):
        for user in self:
            student = self.env['a3.student'].search([('user_id', '=', user.id)])
            if student:
                user.student_id = student[0]
            else:
                user.student_id = False

    def _faculty(self):
        for user in self:
            faculty = self.env['a3.faculty'].search([('user_id', '=', user.id)])
            if faculty:
                user.faculty_id = faculty[0]
            else:
                user.faculty_id = False
    
    def _staff(self):
        for user in self:
            staff = self.env['a3.staff'].search([('user_id', '=', user.id)])
            if staff:
                user.staff_id = staff[0]
            else:
                user.staff_id = False

    def _school_ids(self):
        for user in self:
            user.school_ids = ()
            staff_id = self.env['a3.staff'].search([('user_id', '=', user.id)])
            if staff_id:
                user.school_ids = staff_id.school_ids
            
            faculty_id = self.env['a3.faculty'].search([('user_id', '=', user.id)])
            if faculty_id:
                user.school_ids = [(4, faculty_id.school_id.id)]            
            
    