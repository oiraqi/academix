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

from odoo import api, models, fields
from odoo.exceptions import UserError


class Assessment(models.Model):
	_name = 'ixquality.assessment'
	_description = 'Course Assessment'
	_inherit = 'ix.school.owned'
	_sql_constraints = [('ixquality_assessment_portfolio_program_ukey', 'unique(portfolio_id, program_id)', 'Duplicate assessment of the same program in the same portfolio!')]

	portfolio_id = fields.Many2one('ixquality.portfolio', 'Portfolio', required=True)
	program_id = fields.Many2one('ixcatalog.program', 'Program', required=True)
	nstudents = fields.Integer('Student Population', compute='_nstudents', store=True)
	program_ids = fields.One2many(comodel_name='ixcatalog.program', related='portfolio_id.lms_course_id.program_ids')
	

	@api.depends('portfolio_id', 'program_id')
	def _nstudents(self):
		for rec in self:
			nstudents = 0
			if rec.portfolio_id and rec.program_id:
				for student in rec.portfolio_id.section_id.student_ids:
					if student.program_id == rec.program_id:
						nstudents += 1
			rec.nstudents = nstudents

	acquisition_level = fields.Selection(related='portfolio_id.lms_course_id.acquisition_level')
	used_assessment_technique_ids = fields.Many2many(comodel_name='ixlms.assessment.technique', compute='_uat_ids')

	@api.onchange('portfolio_id')
	def _uat_ids(self):
		for rec in self:
			if not rec.portfolio_id or \
				(not rec.portfolio_id.useful_assessment_technique_ids and \
					not rec.portfolio_id.not_recommended_assessment_technique_ids):
				rec.used_assessment_technique_ids = False
				continue
			
			used_assessment_technique_ids = []
			
			for uat in rec.portfolio_id.useful_assessment_technique_ids:
				used_assessment_technique_ids.append(uat.id)
			
			for uat in rec.portfolio_id.not_recommended_assessment_technique_ids:
				used_assessment_technique_ids.append(uat.id)
			
			rec.used_assessment_technique_ids = used_assessment_technique_ids

	assessment_line_ids = fields.One2many(comodel_name='ixquality.assessment.line', inverse_name='assessment_id', string='Assessment Lines')

	@api.onchange('program_id')
	def _onchange_program_id(self):
		for rec in self:
			rec.assessment_line_ids = False

	course_id = fields.Many2one(comodel_name='ix.course', string='Course', required=True)
	section_id = fields.Many2one('ixroster.section', related='portfolio_id.section_id')
	lms_course_id = fields.Many2one('ixlms.course', related='portfolio_id.lms_course_id')
	faculty_id = fields.Many2one(comodel_name='ix.faculty', related='section_id.instructor_id', store=True)
	ilo_so_ids = fields.One2many(comodel_name='ixquality.lms.course.ilo.so', compute='_ilo_so_ids', string='ILO/SO Mapping')
	assessed_so_ids = fields.One2many(comodel_name='ixquality.student.outcome', compute='_ilo_so_ids', string='Covered/Assessed SOs')
	
	@api.onchange('course_id', 'program_id')
	def _ilo_so_ids(self):
		for rec in self:
			records = self.env['ixquality.lms.course.ilo.so'].search([('course_id', '=', rec.course_id.id), ('program_id', '=', rec.program_id.id)], order="so_id, lms_course_ilo_id")
			if not records:
				rec.ilo_so_ids = False
				rec.assessed_so_ids = False
				continue
			rec.ilo_so_ids = [record.id for record in records]
			assessed_so_ids = []
			for record in records:
				if record.so_id.id not in assessed_so_ids:
					assessed_so_ids.append(record.so_id.id)
			rec.assessed_so_ids = assessed_so_ids
