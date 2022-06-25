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


class Enrollment(models.Model):
    _inherit = 'a3roster.enrollment'

    assessment_line_ids = fields.One2many(comodel_name='a3lms.assessment.line', compute='_assessment_line_ids', string='Assessments')
    attendance_line_absent_ids = fields.One2many(comodel_name='a3lms.attendance.line', compute='_attendance', string='Absences')
    attendance_rate = fields.Float(string='Attendance Rate', compute='_attendance')
    nabsences = fields.Integer(string='Absenses', compute='_attendance')    
    attendance_grade = fields.Float(string='Attendance Grade', compute='_attendance')    

    def _attendance(self):
        for rec in self:
            rec.attendance_line_absent_ids = self.env['a3lms.attendance.line'].search([
                ('section_id', '=', rec.section_id.id), ('student_id', '=', rec.student_id.id),
                ('state', '=', 'absent')])
            rec.nabsences = len(rec.attendance_line_absent_ids)
            all_attendance_count = self.env['a3lms.attendance.line'].search_count([
                ('section_id', '=', rec.section_id.id), ('student_id', '=', rec.student_id.id)])
            rec.attendance_rate = rec.nabsence * 100 / all_attendance_count
            lms_course_id = rec.section_id.lms_course_id
            if lms_course_id.attendance_weight > 0:
                if lms_course_id.zero_after_max_abs and rec.nabsences >= lms_course_id.max_absences:
                    rec.attendance_grade = 0
                elif lms_course_id.attendance_grading == 'rate':
                    rec.attendance_grade = rec.attendance_rate
                elif lms_course_id.attendance_grading == 'penalty':
                    penalty = rec.nabsences * lms_course_id.penalty_per_absence
                    if penalty < 100:
                        rec.attendance_grade = 100 - penalty
                    else:
                        rec.attendance_grade = 0
            
    
    def _assessment_line_ids(self):
        for rec in self:
            rec.assessment_line_ids = self.env['a3lms.assessment.line'].search([
                ('section_id', '=', rec.section_id.id), ('student_id', '=', rec.student_id.id)])
     
    