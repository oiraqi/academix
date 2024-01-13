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


class AttendanceLine(models.Model):
	_name = 'ixlms.attendance.line'
	_description = 'AttendanceLine'
	_order = 'student_id'

	name = fields.Char(related='student_id.name')	
	student_id = fields.Many2one(comodel_name='ix.student', string='Student', required=True)	
	attendance_id = fields.Many2one(comodel_name='ixlms.attendance', string='Attendance', required=True)
	section_id = fields.Many2one(comodel_name='ixroster.section', related='attendance_id.section_id', store=True)	
	state = fields.Selection(string='State', selection=[('present', 'Present'), ('absent', 'Absent - Unexcused'), ('late', 'Late'), ('absentx', 'Absent - Excused')], default='present', required=True)
	program_id = fields.Many2one(comodel_name='ixcatalog.program', string='Program', related='student_id.program_id', store=True)
	school_id = fields.Many2one(comodel_name='ix.school', string='School', related='attendance_id.section_id.school_id', store=True)
	day = fields.Date(related='attendance_id.day', store=True)
		