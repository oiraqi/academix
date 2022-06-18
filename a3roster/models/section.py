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
from odoo.exceptions import UserError


class Section(models.Model):
    _name = 'a3roster.section'
    _description = 'Course Section'
    _inherit = ['a3.school.activity', 'a3.calendarized']
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
    start_timeslot = fields.Float(string='Start Time', required=True)
    end_timeslot = fields.Float(string='End Time', required=True)
    monday = fields.Boolean(string='M', default=False)
    tuesday = fields.Boolean(string='T', default=False)
    wednesday = fields.Boolean(string='W', default=False)
    thursday = fields.Boolean(string='R', default=False)
    friday = fields.Boolean(string='F', default=False)
    days = fields.Char(compute='_timeslot')    
    timeslot = fields.Char('Timeslot', compute='_timeslot')
    syllabus = fields.Binary(string='Syllabus')
    capacity = fields.Integer(string='Capacity', default=24, required=True)    
    student_ids = fields.One2many('a3.student', compute='_student_ids', string='Students')
    active_enrollment_ids = fields.One2many('a3roster.enrollment', compute='_active_enrollment_ids', string='Dropped Students')
    dropped_enrollment_ids = fields.One2many('a3roster.enrollment', compute='_dropped_enrollment_ids', string='Dropped Students')
    withdrawn_enrollment_ids = fields.One2many('a3roster.enrollment', compute='_withdrawn_enrollment_ids', string='Withdrawn Students')
    is_open = fields.Boolean(string='Open', compute='_is_open')
    
    def _is_open(self):
        for rec in self:
            if not rec.student_ids:
                rec.is_open = True
            else:
                rec.is_open = len(rec.student_ids) < rec.capacity
    
    def _student_ids(self):
        for rec in self:
            enrollment_ids = self.env['a3roster.enrollment'].search([('section_id', '=', rec.id), ('state', '=', 'enrolled')])
            if enrollment_ids:
                rec.student_ids = [enrollment.student_id.id for enrollment in enrollment_ids]
            else:
                rec.student_ids = False

    def _active_enrollment_ids(self):
        for rec in self:
            enrollment_ids = self.env['a3roster.enrollment'].search([('section_id', '=', rec.id), ('state', '=', 'enrolled')])
            if enrollment_ids:
                rec.active_enrollment_ids = enrollment_ids
            else:
                rec.active_enrollment_ids = False
    
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

    @api.depends('start_timeslot', 'end_timeslot', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday')
    @api.onchange('start_timeslot', 'end_timeslot', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday')
    def _timeslot(self):
        for rec in self:
            days = ''
            if rec.monday:
                days = 'M'
            if rec.tuesday:
                days += 'T'
            if rec.wednesday:
                days += 'W'
            if rec.thursday:
                days += 'R'
            if rec.friday:
                days += 'F'
            rec.days = days
            if days == '':
                rec.timeslot = ''
                continue
            
            if rec.start_timeslot and rec.end_timeslot and rec.end_timeslot > rec.start_timeslot:
                start_hours = int(rec.start_timeslot)
                start_minutes = int((rec.start_timeslot - start_hours) * 60)
                if start_hours < 10:
                    start_hours = '0' + str(start_hours)
                else:
                    start_hours = str(start_hours)                
                if start_minutes < 10:
                    start_minutes = '0' + str(start_minutes)
                start_time = start_hours + ':' + str(start_minutes)
                
                end_hours = int(rec.end_timeslot)
                end_minutes = int((rec.end_timeslot - end_hours) * 60)
                if end_hours < 10:
                    end_hours = '0' + str(end_hours)
                else:
                    end_hours = str(end_hours)                
                if end_minutes < 10:
                    end_minutes = '0' + str(end_minutes)
                else:
                    end_minutes = str(end_minutes)
                end_time = end_hours + ':' + end_minutes
                rec.timeslot = days + ' ' + start_time + ' - ' + end_time
            else:
                rec.timeslot = ''

    @api.constrains('start_timeslot', 'start_timeslot')
    def _constrains_start_timeslot(self):
        for rec in self:
            if rec.start_timeslot >= rec.end_timeslot or rec.start_timeslot < 8 or rec.start_timeslot >= 24 or rec.end_timeslot < 8 or rec.end_timeslot >= 24:
                raise UserError('Error in timeslot')
    