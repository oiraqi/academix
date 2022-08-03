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


class Enrollment(models.Model):
    _inherit = 'ixroster.enrollment'

    assessment_line_ids = fields.One2many(comodel_name='ixlms.assessment.line', compute='_assessment_line_ids', string='Assessments')
    attendance_line_absent_late_ids = fields.One2many(comodel_name='ixlms.attendance.line', compute='_attendance', string='Absences')
    attendance_rate = fields.Float(string='Attendance Rate (%)', compute='_attendance')
    nabsences = fields.Integer(string='Unexcused Absenses', compute='_attendance')
    nxabsences = fields.Integer(string='Excused Absenses', compute='_attendance')
    nlates = fields.Integer(string='Times Late', compute='_attendance')
    attendance_grade = fields.Float(string='Attendance Grade', compute='_attendance')
    assessment_grade = fields.Float(string='Assessment Grade', compute='_grade')
    overall_grade = fields.Float(string='Overall Grade (%)', compute='_grade')
    letter_grade = fields.Char(string='Letter Grade', compute='_grade')
    passed = fields.Boolean(string='Passed', compute='_grade')

    def _grade(self):
        for rec in self:
            lms_course_id = rec.section_id.lms_course_id
            rec.assessment_grade, assessment_weight = rec._assessment_grade(lms_course_id)
            if lms_course_id.attendance_weight > 0:
                rec.overall_grade = (rec.assessment_grade * assessment_weight + rec.attendance_grade * lms_course_id.attendance_weight) / (assessment_weight + lms_course_id.attendance_weight)
            else:
                rec.overall_grade = rec.assessment_grade
            rec.letter_grade, rec.passed = self.env['ixlms.letter.grade'].evaluate(rec.overall_grade)            

    def _assessment_grade(self, lms_course_id):
        if lms_course_id.grade_weighting == 'percentage':
            sum_epercentage, sum_wgrade = 0.0, 0.0            
            for assessment_line in self.assessment_line_ids:
                if assessment_line.epercentage > 0:
                    sum_epercentage += assessment_line.epercentage
                    sum_wgrade += assessment_line.wgrade            
            if sum_epercentage > 0:
                return fields.Float.round((sum_wgrade / sum_epercentage) * 100, 2), sum_epercentage
            return 0.0, 0.0
        
        if lms_course_id.grade_weighting == 'points':
            sum_epoints, sum_wgrade = 0.0, 0.0
            for assessment_line in self.assessment_line_ids:
                if assessment_line.sum_epoints > 0:
                    sum_epoints += assessment_line.epoints
                    sum_wgrade += assessment_line.wgrade
            if sum_epoints > 0:
                return fields.Float.round(sum_wgrade / sum_epoints * 100, 2), sum_epoints
            return 0.0, 0.0       
        
        return 0.0, 0.0    

    def _attendance(self):
        for rec in self:
            rec.attendance_line_absent_late_ids = self.env['ixlms.attendance.line'].search([
                ('section_id', '=', rec.section_id.id), ('student_id', '=', rec.student_id.id),
                ('state', 'in', ['absent', 'absentx', 'late'])])
            rec.nabsences = self.env['ixlms.attendance.line'].search_count([
                ('section_id', '=', rec.section_id.id), ('student_id', '=', rec.student_id.id),
                ('state', '=', 'absent')])
            rec.nxabsences = self.env['ixlms.attendance.line'].search_count([
                ('section_id', '=', rec.section_id.id), ('student_id', '=', rec.student_id.id),
                ('state', '=', 'absentx')])
            rec.nlates = self.env['ixlms.attendance.line'].search_count([
                ('section_id', '=', rec.section_id.id), ('student_id', '=', rec.student_id.id),
                ('state', '=', 'late')])
            all_attendance_count = self.env['ixlms.attendance.line'].search_count([
                ('section_id', '=', rec.section_id.id), ('student_id', '=', rec.student_id.id)])
            if all_attendance_count != 0:
                rec.attendance_rate = 100 - rec.nabsences * 100 / all_attendance_count
            else:
                rec.attendance_rate = 100
            lms_course_id = rec.section_id.lms_course_id
            rec.attendance_grade = 100
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
            rec.assessment_line_ids = self.env['ixlms.assessment.line'].search([
                ('section_id', '=', rec.section_id.id), ('student_id', '=', rec.student_id.id)])
     
    