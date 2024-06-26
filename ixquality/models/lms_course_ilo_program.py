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


class LmsCourseIloProgram(models.Model):
	_name = 'ixquality.lms.course.ilo.program'
	_description = 'Lms Course ILO Program'
	_sql_constraints = [('lms_course_ilo_program_ukey', 'unique(lms_course_id, lms_course_ilo_id, program_id)', 'Duplicate Course/ILO/Program lines!')]
	_order = 'lms_course_ilo_id'

	@api.model
	def create(self, vals):
		lms_course_ilo_program = super(LmsCourseIloProgram, self).create(vals)
		ilo_so_ids = self.env['ixquality.course.ilo.so'].search([('course_id', '=', lms_course_ilo_program.lms_course_id.course_id.id), ('program_id', '=', lms_course_ilo_program.program_id.id), ('ilo_id.sequence', '=', lms_course_ilo_program.lms_course_ilo_id.sequence)])
		for ilo_so in ilo_so_ids:
			if not self.env['ixquality.lms.course.ilo.so'].search([('lms_course_ilo_id', '=', lms_course_ilo_program.lms_course_ilo_id.id),
					('so_id', '=', ilo_so.so_id.id), ('course_program_id', '=', ilo_so.course_program_id.id)]):
				self.env['ixquality.lms.course.ilo.so'].create({
		            'lms_course_ilo_id': lms_course_ilo_program.lms_course_ilo_id.id,
    		        'so_id': ilo_so.so_id.id,
        		    'course_program_id': ilo_so.course_program_id.id,
            		'level': ilo_so.level,
        		})
		return lms_course_ilo_program

	lms_course_id = fields.Many2one(comodel_name='ixlms.course', string='Course', required=True)		
	lms_course_ilo_id = fields.Many2one(comodel_name='ixlms.course.ilo', string='Course ILO', required=True)
	program_id = fields.Many2one(comodel_name='ixcatalog.program', string='Program', required=True)	
	percentage = fields.Float(string='Students who reached TAL (%)', compute='_percentage')
	count = fields.Integer(string='Assessed Students', compute='_percentage')

	def _percentage(self):
		for rec in self:
			s, c, a = {}, {}, 0
			assessed_ilos = self.env['ixquality.assessed.ilo'].search([('lms_course_id', '=', rec.lms_course_id.id), ('program_id', '=', rec.program_id.id), ('lms_course_ilo_id', '=', rec.lms_course_ilo_id.id)])
			for assessed_ilo in assessed_ilos:
				if str(assessed_ilo.student_id) in s:
					s[str(assessed_ilo.student_id)] += int(assessed_ilo.acquisition_level)
					c[str(assessed_ilo.student_id)] += 1
				else:
					s[str(assessed_ilo.student_id)] = int(assessed_ilo.acquisition_level)
					c[str(assessed_ilo.student_id)] = 1

			rec.count = len(s)
			if len(s) > 0:
				for t in s:
					if s[t]/c[t] >= int(rec.lms_course_id.acquisition_level):
						a += 1
				rec.percentage = fields.Float.round(100 * a / len(s), 2)
			else:
				rec.percentage = 0

	