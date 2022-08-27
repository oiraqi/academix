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


class Attendance(models.Model):
	_name = 'ixlms.attendance'
	_description = 'Attendance'
	_order = 'day'
	_sql_constraints = [('section_day_ukey', 'unique(section_id, day)', 'Attendance sheet already exists')]

	name = fields.Char('Name', compute='_set_name')
	course_id = fields.Many2one(comodel_name='ixlms.course', string='Course', required=True)
	lms_course_id = fields.Many2one(comodel_name='ixlms.course', related='course_id', store=True)
	section_id = fields.Many2one(comodel_name='ixroster.section', related='course_id.section_id', store=True)
	term_id = fields.Many2one(comodel_name='ix.term', related='course_id.section_id.term_id', store=True)
	school_id = fields.Many2one(comodel_name='ix.school', related='course_id.section_id.school_id', store=True)
	instructor_id = fields.Many2one(comodel_name='ix.faculty', related='course_id.section_id.instructor_id', store=True)
	day = fields.Date(string='Date', required=True, default= lambda self: fields.Date.today())
	attendance_line_ids = fields.One2many(comodel_name='ixlms.attendance.line', inverse_name='attendance_id', string='Attendance Lines')
	npresent = fields.Integer(string='Present', compute='_stats')
	nabsent = fields.Integer(string='Absent - Unexcused', compute='_stats')
	nabsentx = fields.Integer(string='Absent - Excused', compute='_stats')
	nlate = fields.Integer(string='Late', compute='_stats')
	
	@api.onchange('attendance_line_ids')
	def _stats(self):
		for rec in self:
			if rec.attendance_line_ids:
				npresent = nabsent = nabsentx = nlate = 0
				for line in rec.attendance_line_ids:
					if line.state == 'present':
						npresent += 1
					elif line.state == 'absent':
						nabsent += 1
					elif line.state == 'absentx':
						nabsentx += 1
					elif line.state == 'late':
						nlate += 1
				rec.npresent = npresent
				rec.nabsent = nabsent
				rec.nabsentx = nabsentx
				rec.nlate = nlate
			else:
				rec.npresent = 0
				rec.nabsent = 0
				rec.nabsentx = 0
				rec.nlate = 0
	
	
	def _set_name(self):
		for rec in self:
			if rec.course_id and rec.day:
				rec.name = 'Attendance / ' + rec.course_id.name + ' / ' + fields.Date.to_string(rec.day)
			else:
				rec.name = ''

	@api.onchange('course_id', 'day')
	def _onchange_course_id(self):
		for rec in self:
			if rec.day and rec.course_id and rec.course_id.student_ids and not rec.attendance_line_ids:
				for student in rec.course_id.student_ids:
					rec.attendance_line_ids += self.env['ixlms.attendance.line'].new({
						'student_id': student.id,
						'attendance_id': rec.id,
						'state': 'present',
					})
