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


class Student(models.Model):
    _inherit = 'a3.student'    

    attendance_line_absent_ids = fields.One2many(comodel_name='a3lms.attendance.line', compute='_attendance_line_absent_ids', string='Missed Classes')

    def _attendance_line_absent_ids(self):
        for rec in self:
            rec.attendance_line_absent_ids = self.env['a3lms.attendance.line'].search([
                ('student_id', '=', rec.student_id.id), ('state', '=', 'absent')])
     
    