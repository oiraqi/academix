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
    _inherit = 'ix.student'    

    attendance_line_absent_ids = fields.One2many(comodel_name='ixlms.attendance.line', compute='_attendance_line_absent_ids', string='Missed Classes')
    earned_sch = fields.Integer(compute='_sch', string='Earned Credits')
    remaining_sch = fields.Integer(compute='_sch', string='Remaining Credits')
    progress = fields.Float(string='Progress', compute='_sch')
    

    def _sch(self):
        for rec in self:
            earned_sch = 0
            for enrollment in rec.enrollment_ids:
                if enrollment.state == 'completed' and enrollment.passed:
                    earned_sch += enrollment.course_id.sch
            rec.earned_sch = earned_sch
            rec.remaining_sch = rec.program_sch - earned_sch
            if rec.program_sch == 0:
                rec.progress = 0
            else:
                rec.progress = float(rec.earned_sch) * 100 / rec.program_sch

    def _attendance_line_absent_ids(self):
        for rec in self:
            rec.attendance_line_absent_ids = self.env['ixlms.attendance.line'].search([
                ('student_id', '=', rec.id), ('state', '=', 'absent')])
     
    