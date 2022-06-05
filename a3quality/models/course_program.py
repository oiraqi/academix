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


class CourseProgram(models.Model):
    _name = 'a3quality.course.program'
    _description = 'Course Program Mapping'
    _sql_constraints = [('course_program_ukey', 'unique(course_id, program_id)', 'Course/Program mapping already exists')]

    course_id = fields.Many2one(comodel_name='a3.course', string='Course', required=True)
    program_id = fields.Many2one(comodel_name='a3catalog.program', string='Program', required=True)
    ilo_so_ids = fields.One2many(comodel_name='a3quality.course.ilo.so', inverse_name='course_program_id', string='Mapping')
    discipline_id = fields.Many2one(comodel_name='a3.discipline', related='course_id.discipline_id', store=True)
    school_id = fields.Many2one(comodel_name='a3.school', related='course_id.school_id', store=True)
    ilo_ids = fields.One2many('a3catalog.course.ilo', related='course_id.ilo_ids', string="Course ILOs")
    so_ids = fields.One2many('a3quality.student.outcome', related='program_id.so_ids', string="Program SOs")
    covered_so_ids = fields.One2many(comodel_name='a3quality.student.outcome', compute='_covered_so_ids', string='Covered/Assessed SOs')

    def _covered_so_ids(self):
        for rec in self:
            if not rec.ilo_so_ids:
                rec.covered_so_ids = False
                continue
            rec.covered_so_ids = [record.so_id.id for record in rec.ilo_so_ids]
    

    @api.onchange('course_id', 'program_id')
    def _onchange_course_program(self):
        for rec in self:
            rec.ilo_so_ids = False
    
    @api.onchange('course_id')
    def _onchange_course(self):
        for rec in self:
            rec.program_id = False
    
    