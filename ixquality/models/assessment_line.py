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


class AssessmentLine(models.Model):
	_name = 'ixquality.assessment.line'
	_description = 'AssessmentLine'
	_sql_constraints = [('assessment_ilo_ukey', 'unique(assessment_id, lms_course_ilo_id)', 'Duplicate ILO assessment')]

	assessment_id = fields.Many2one('ixquality.assessment', 'Assessment', required=True)
	course_id = fields.Many2one(comodel_name='ix.course', related='assessment_id.course_id')
	lms_course_id = fields.Many2one('ixlms.course', related='assessment_id.lms_course_id')
	faculty_id = fields.Many2one(comodel_name='ix.faculty', related='assessment_id.faculty_id', store=True)	
	lms_course_ilo_id = fields.Many2one('ixlms.course.ilo', 'ILO', required=True)
	so_ids = fields.One2many('ixquality.student.outcome', compute='_so_ids', string='SOs')
	assessment_ids = fields.One2many(comodel_name='ixlms.assessment', compute='_assessment_ids', string="Assessments")

	@api.onchange('assessment_id', 'lms_course_ilo_id')
	def _assessment_ids(self):
		for rec in self:
			assessment_ids = []
			for assessment in rec.assessment_id.portfolio_id.lms_course_id.assessment_ids:
				if rec.lms_course_ilo_id in assessment.lms_course_ilo_ids:
					assessment_ids.append(assessment.id)
			if len(assessment_ids) > 0:
				rec.assessment_ids = assessment_ids
			else:
				rec.assessment_ids = False
					

	sos = fields.Char(compute='_sos')

	def _sos(self):
		for rec in self:
			sos = ''
			if rec.so_ids:
				if len(rec.so_ids) == 1:
					sos = rec.so_ids[0].name
				else:
					sos = ', '.join([so.name for so in rec.so_ids])
			rec.sos = sos

	assessments = fields.Char(compute='_assessments')

	def _assessments(self):
		for rec in self:
			assessments = ''
			if rec.assessment_ids:
				if len(rec.assessment_ids) == 1:
					assessments = rec.assessment_ids[0].name
				else:
					assessments = ', '.join([assessment.name for assessment in rec.assessment_ids])
			rec.assessments = assessments

	targetted = fields.Selection(string='Targetted', selection=[
		('70', '70'), ('75', '75'), ('80', '80'),
		('85', '85'), ('90', '90'), ('95', '95'), ('100', '100')], default='80', required=True)
	achieved = fields.Float('Achieved', compute='_achieved')

	@api.onchange('assessment_id', 'lms_course_ilo_id')
	def _achieved(self):
		for rec in self:
			result = self.env['ixquality.lms.course.ilo.program'].search([('lms_course_id', '=', rec.assessment_id.portfolio_id.lms_course_id.id), ('program_id', '=', rec.assessment_id.program_id.id), ('lms_course_ilo_id', '=', rec.lms_course_ilo_id.id)])
			if result:
				rec.achieved = result.percentage
			else:
				rec.achieved = 0

	action_id = fields.Many2one('ixquality.action', 'Action')

	@api.onchange('lms_course_ilo_id', 'assessment_id')
	def _so_ids(self):
		for rec in self:
			if not rec.lms_course_ilo_id or not rec.assessment_id:
				rec.so_ids = False
				continue
			
			records = self.env['ixquality.lms.course.ilo.so'].search([
				('course_program_id.program_id', '=', rec.assessment_id.program_id.id),
				('lms_course_ilo_id', '=', rec.lms_course_ilo_id.id)])
			if not records:
				rec.so_ids = False
			else:
				rec.so_ids = [record.so_id.id for record in records]
