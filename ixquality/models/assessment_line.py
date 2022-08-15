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


class AssessmentLine(models.Model):
	_name = 'ixquality.assessment.line'
	_description = 'AssessmentLine'
	_sql_constraints = [('assessment_ilo_ukey', 'unique(assessment_id, ilo_id)', 'Duplicate ILO assessment')]

	assessment_id = fields.Many2one('ixquality.assessment', 'Assessment', required=True)
	course_id = fields.Many2one(comodel_name='ix.course', related='assessment_id.course_id')
	faculty_id = fields.Many2one(comodel_name='ix.faculty', related='assessment_id.faculty_id', store=True)	
	ilo_id = fields.Many2one('ixcatalog.course.ilo', 'ILO', required=True)
	so_ids = fields.One2many('ixquality.student.outcome', compute='_so_ids', string='SOs')
	assessment_technique_ids = fields.One2many(comodel_name='ixlms.assessment.technique', compute='_assessment_technique_ids')

	@api.onchange('assessment_id')
	def _assessment_technique_ids(self):
		for rec in self:
			technique_ids = []
			for assessment in rec.assessment_id.portfolio_id.lms_course_id.assessment_ids:
				if rec.ilo_id in assessment.ilo_ids and assessment.technique_id.technique_id.id not in technique_ids:
					technique_ids.append(assessment.technique_id.technique_id.id)
			if len(technique_ids) > 0:
				rec.assessment_technique_ids = technique_ids
			else:
				rec.assessment_technique_ids = False
					


	targetted = fields.Selection(string='Targetted', selection=[
		('70', '70'), ('75', '75'), ('80', '80'),
		('85', '85'), ('90', '90'), ('95', '95'), ('100', '100')], default='80', required=True)
	achieved = fields.Float('Achieved', required=True)

	@api.constrains('achieved')
	def _achieved(self):
		for rec in self:
			if rec.achieved < 0 or rec.achieved > 100:
				raise UserError('Achieved must be between 0 and 100')

	action_id = fields.Many2one('ixquality.action', 'Action')

	@api.onchange('ilo_id', 'assessment_id')
	def _so_ids(self):
		for rec in self:
			if not rec.ilo_id or not rec.assessment_id:
				rec.so_ids = False
				continue
			
			records = self.env['ixquality.course.ilo.so'].search([
				('course_program_id.program_id', '=', rec.assessment_id.program_id.id),
				('ilo_id', '=', rec.ilo_id.id)])
			if not records:
				rec.so_ids = False
			else:
				rec.so_ids = [record.so_id.id for record in records]
