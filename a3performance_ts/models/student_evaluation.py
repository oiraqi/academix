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


SEMESTERS = {'1': 'FA', '2': 'SP', '3': 'SU'}


class StudentEvaluation(models.Model):
    _name = 'ixperformance.ts.student.evaluation'
    _inherit = 'ix.faculty.activity'

    @api.model
    def _nstudent_selection(self):
        nstudent_list = []
        i = 1
        while i <= 40:
            nstudent_list.append((str(i), str(i)))
            i += 1
        return nstudent_list

    name = fields.Char(compute='_compute_name')

    @api.depends('section_id')
    @api.onchange('section_id')
    def _compute_name(self):
        for rec in self:
            if rec.section_id:
                rec.name = rec.section_id.name
            else:
                rec.name = ''

    section_id = fields.Many2one(
        'ixroster.section', string='Section', required=True)
    level = fields.Selection(
        related='section_id.course_id.level', readonly=True, store=True)
    nstudents = fields.Selection(
        _nstudent_selection, 'Number of Students', default='20', required=True)
    score = fields.Float('Score', required=True, group_operator='avg')
    student_feedback = fields.Html('Student Feedback')

    @api.onchange('year', 'semester')
    def _se_onchange_year_semester(self):
        for rec in self:
            if rec.year and rec.semester:
                sections = self.env['ixroster.section'].search(
                    [('instructor_id.user_id', '=', self.env.user.id), ('year', '=', rec.year),
                    ('semester', '=', rec.semester)])
                if sections:
                    rec.section_id = sections[0]
                else:
                    rec.section_id = False
