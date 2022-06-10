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
    _inherit = 'a3.school.activity'
    _order = 'course_id,number'
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
    start_time = fields.Float(string='Start Time', required=True)
    end_time = fields.Float(string='End Time', required=True)
    monday = fields.Boolean(string='M', default=False)
    tuesday = fields.Boolean(string='T', default=False)
    wednesday = fields.Boolean(string='W', default=False)
    thursday = fields.Boolean(string='R', default=False)
    friday = fields.Boolean(string='F', default=False)
    timeslot = fields.Char('Timeslot', compute='_timeslot')
    classroom_id = fields.Many2one(comodel_name='a3.room', string='Classroom')
    syllabus = fields.Binary(string='Syllabus')    
    student_ids = fields.Many2many('a3.student', 'a3roster_section_student_rel', 'section_id', 'student_id', 'Students')        

    @api.depends('start_time', 'end_time', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday')
    @api.onchange('start_time', 'end_time', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday')
    def _timeslot(self):
        for rec in self:
            if rec.start_time and rec.end_time and rec.end_time > rec.start_time:
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
                if days == '':
                    rec.timeslot = ''
                    continue
                start_hours = int(rec.start_time)
                start_minutes = (rec.start_time - start_hours) * 60
                start_time = str(start_hours) + ':' + str(start_minutes)
                end_hours = int(rec.end_time)
                end_minutes = (rec.end_time - end_hours) * 60
                end_time = str(end_hours) + ':' + str(end_minutes)
                rec.timeslot = days + ' ' + start_time + ' - ' + end_time
            else:
                rec.timeslot = ''
    