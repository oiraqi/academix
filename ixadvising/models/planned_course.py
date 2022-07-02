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

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PlannedCourse(models.Model):
    _name = 'ixadvising.planned.course'
    _description = 'Planned Course'
    _inherit = ['ix.student.owned', 'ix.activity']
    _sql_constraints = [('course_student_ukey', 'unique(course_id, student_id)', 'Course already planned!')]

    course_id = fields.Many2one(comodel_name='ix.course', string='Course', required=True)
    prerequisite_ids = fields.One2many('ixcatalog.prerequisite', related='course_id.prerequisite_ids')
    corequisite_ids = fields.One2many('ixcatalog.corequisite', related='course_id.corequisite_ids')
    prerequisite_for_ids = fields.One2many('ix.course', related='course_id.prerequisite_for_ids')
    corequisite_for_ids = fields.One2many('ix.course', related='course_id.corequisite_for_ids')
    name = fields.Char(string='Name', compute='_set_name')
    description = fields.Html(related='course_id.description')
    section_id = fields.Many2one(comodel_name='ixroster.section', string='Section')
    timeslot = fields.Char(related='section_id.timeslot')    
    enrollment_id = fields.Many2one(comodel_name='ixroster.enrollment', string='Enrollment')
    state = fields.Selection(related='enrollment_id.state')    
    # grade = fields.Char(related='enrollment_id.letter_grade')
    # passed = fields.Boolean(related='enrollment_id.passed')

    @api.constrains('term_id')
    def _check_max_credits(self):
        for rec in self:
            records = self.env['ixadvising.planned.course'].search(
                [('term_id', '=', rec.term_id.id)])
            if records:
                sum_credits = sum([record.course_id.sch for record in records])
                if sum_credits > 18:# To do: should depend on student credit limit / semester
                    raise ValidationError('Max allowed number of credits (18) exceeded!')
            
    @api.constrains('term_id')
    def _check_prerequisites(self):# Incomplete
        for rec in self:
            records = self.env['ixadvising.planned.course'].search(
                ['|', ('year', '<', rec.year), '&', ('year', '=', rec.year), ('semester', '<', rec.semester)]
            )
            planned_courses = [record.course_id.id for record in records]
            prerequisites = rec.course_id.prerequisite_ids
            for prerequisite in prerequisites:
                satisfied = False
                unsatisfied = ''
                for alternative in prerequisite.alternative_ids:
                    if unsatisfied:
                        unsatisfied += ', or '
                    unsatisfied += alternative.name
                    if alternative.id in planned_courses:
                        satisfied = True
                        break
                if not satisfied:
                    raise ValidationError('Prerequisite ' + unsatisfied + ': Unsatisfied!')

    
    @api.onchange('course_id')
    def _set_name(self):
        for rec in self:
            if rec.course_id:
                rec.name = rec.course_id.name


    def preregister(self):
        self.enrollment_id = self.env['ixroster.enrollment'].create({
            'student_id': self.student_id.id,
            'section_id': self.section_id.id
        })
        self.enrollment_id.enroll()