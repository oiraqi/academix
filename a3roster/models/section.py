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


class Section(models.Model):
    _name = 'a3roster.section'
    _description = 'Course Section'
    _inherit = ['a3.school.activity', 'a3.calendarized', 'a3roster.scheduled']
    _order = 'year desc,semester desc,course_id,number'
    _sql_constraints = [('section_ukey', 'unique(year, semester, course_id, number)', 'Section already exists')]

    name = fields.Char(compute='_compute_name', string='Name', store=True)
    
    @api.depends('course_id', 'number', 'year', 'semester')
    @api.onchange('course_id', 'number', 'year', 'semester')
    def _compute_name(self):
        for rec in self:
            if rec.course_id and rec.number and rec.year and rec.semester:
                rec.name = rec.prefix + rec.course_id.code.replace(' ', '') + rec.number
            else:
                rec.name = ''
    
    course_id = fields.Many2one(comodel_name='a3.course', string='Course', required=True)    
    number = fields.Selection(string='Section', selection=[('01', '01'), ('02', '02'),
                                                          ('03', '03'), ('04', '04'),
                                                          ('05', '05'), ('06', '06'),
                                                          ('07', '07'), ('08', '08'),
                                                          ('09', '09'), ('10', '10')], default='01', required=True)
    discipline_id = fields.Many2one(comodel_name='a3.discipline', string='Discipline', required=True)
    instructor_id = fields.Many2one(comodel_name='a3.faculty', string='Instructor')
    
    syllabus = fields.Binary(string='Syllabus')
    capacity = fields.Integer(string='Capacity', default=24, required=True)    
    student_ids = fields.One2many('a3.student', compute='_active_enrollment_ids', string='Students')
    active_enrollment_ids = fields.One2many('a3roster.enrollment', compute='_active_enrollment_ids', string='Dropped Students')
    dropped_enrollment_ids = fields.One2many('a3roster.enrollment', compute='_dropped_enrollment_ids', string='Dropped Students')
    withdrawn_enrollment_ids = fields.One2many('a3roster.enrollment', compute='_withdrawn_enrollment_ids', string='Withdrawn Students')
    is_open = fields.Boolean(string='Open', compute='_is_open')
    nstudents = fields.Integer(string='Enrolled Students', compute='_active_enrollment_ids')
    available_seats = fields.Integer(string='Available Seats', compute='_active_enrollment_ids')    
    
    def _is_open(self):
        for rec in self:
            if not rec.student_ids:
                rec.is_open = True
            else:
                rec.is_open = len(rec.student_ids) < rec.capacity

    @api.onchange('capacity')
    def _active_enrollment_ids(self):
        for rec in self:
            enrollment_ids = self.env['a3roster.enrollment'].search([('section_id', '=', rec.id), ('state', '=', 'enrolled')])
            if enrollment_ids:
                rec.student_ids = [enrollment.student_id.id for enrollment in enrollment_ids]
                rec.active_enrollment_ids = enrollment_ids                
            else:
                rec.student_ids = False
                rec.active_enrollment_ids = False
            rec.nstudents = len(enrollment_ids)
            rec.available_seats = rec.capacity - rec.nstudents
    
    def _dropped_enrollment_ids(self):
        for rec in self:
            enrollment_ids = self.env['a3roster.enrollment'].search([('section_id', '=', rec.id), ('state', '=', 'dropped')])
            if enrollment_ids:
                rec.dropped_enrollment_ids = enrollment_ids
            else:
                rec.dropped_enrollment_ids = False

    def _withdrawn_enrollment_ids(self):
        for rec in self:
            enrollment_ids = self.env['a3roster.enrollment'].search([('section_id', '=', rec.id), ('state', '=', 'withdrawn')])
            if enrollment_ids:
                rec.withdrawn_enrollment_ids = enrollment_ids
            else:
                rec.withdrawn_enrollment_ids = False
    
