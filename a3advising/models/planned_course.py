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
    _name = 'a3advising.planned.course'
    _description = 'Planned Course'
    _inherit = ['a3.student.owned', 'a3.activity']
    _sql_constraints = [('course_student_ukey', 'unique(course_id, student_id)', 'Course already planned!')]

    course_id = fields.Many2one(comodel_name='a3.course', string='Course', required=True)
    name = fields.Char(string='Name', compute='_set_name')
    description = fields.Html(related='course_id.description')
    grade = fields.Selection(string='Grade', selection=[('p', 'P'), ('f', 'F')], default='p')


    @api.constrains('term_id')
    def _check_max_courses(self):
        for rec in self:
            if self.env['a3advising.planned.course'].search_count(
                [('term_id', '=', rec.term_id.id)]) > 6:
                raise ValidationError('Max allowed number of courses exceeded!')

    
    @api.onchange('course_id')
    def _set_name(self):
        for rec in self:
            if rec.course_id:
                rec.name = rec.course_id.name

