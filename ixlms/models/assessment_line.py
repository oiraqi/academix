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
from odoo.exceptions import ValidationError


class AssessmentLine(models.Model):
	_name = 'ixlms.assessment.line'
	_description = 'AssessmentLine'
	_inherit = 'ix.expandable'
	_order = 'student_id,assessment_id'
	_sql_constraints = [('student_assessment_ukey', 'unique(student_id, assessment_id)', 'Assessment line already exists')]

	name = fields.Char('Name', related='student_id.name', store=True)
	student_id = fields.Many2one(comodel_name='ix.student', string='Student', required=True)	
	assessment_id = fields.Many2one(comodel_name='ixlms.assessment', string='Assessment', required=True)
	program_id = fields.Many2one(comodel_name='ixcatalog.program', related='student_id.program_id', store=True)	
	lms_course_id = fields.Many2one(comodel_name='ixlms.course', related='assessment_id.lms_course_id', store=True)
	section_id = fields.Many2one(comodel_name='ixroster.section', string='Section', required=True)
	module_id = fields.Many2one(comodel_name='ixlms.module', related='assessment_id.module_id', store=True)
	technique_id = fields.Many2one(comodel_name='ixlms.weighted.technique', related='assessment_id.technique_id', store=True)
	grade_grouping = fields.Selection(related='lms_course_id.grade_grouping', store=True)
	grade_weighting = fields.Selection(related='lms_course_id.grade_weighting', store=True)
	points = fields.Integer(related='assessment_id.points', store=True)
	epoints = fields.Integer(string="Points", compute='_epoints', store=True)

	@api.depends('grade', 'points')
	def _epoints(self):
		for rec in self:
			if rec.grade:
				rec.epoints = rec.points
			else:
				rec.epoints = 0.0

	module_percentage = fields.Float(related='module_id.percentage', store=True)
	technique_percentage = fields.Float(related='technique_id.percentage', store=True)
	assessment_percentage = fields.Float(related='assessment_id.percentage', store=True)
	percentage = fields.Float(related='assessment_id.percentage', store=True)
	epercentage = fields.Float(string="%", compute='_epercentage', store=True)

	@api.depends('grade', 'percentage')
	def _epercentage(self):
		for rec in self:
			if rec.grade:
				rec.epercentage = rec.percentage
			else:
				rec.epercentage = 0.0

	bonus = fields.Float(related='assessment_id.bonus', store=True)

	def _madeup_assessment_line_ids(self):
		self.madeup_assessment_line_ids = self.env['ixlms.assessment.line'].search([('student_id', '=', self.student_id.id), ('assessment_id', 'in', self.assessment_id.madeup_assessment_ids.ids)])
	
	submission_type = fields.Selection(related='assessment_id.submission_type')
	teamwork = fields.Boolean(related='assessment_id.teamwork')
	submission_ids = fields.Many2many('ixlms.assessment.submission', 'ixlms_assessment_line_submission', 'assessment_line_id', 'submission_id', string='Submissions')
	grade = fields.Char(string='Assigned Grade', default='')
	mgrade = fields.Char(string='Assigned Make-up Grade', default='')
	makeup_grade_policy = fields.Selection(related='assessment_id.makeup_grade_policy')
	makeup_grade_upper_bound = fields.Float(related='assessment_id.makeup_grade_upper_bound')
	madeup_assessment_line_ids = fields.One2many(comodel='ixlms.assessment.line', string='Madeup Assessment Lines', compute='_madeup_assessment_line_ids')

	@api.constrains('grade', 'mgrade')
	def _check_grade(self):
		for rec in self:
			try:
				if (rec.grade and float(rec.grade) < 0) or (rec.mgrade and float(rec.mgrade) < 0):
					raise ValidationError('Grade must be a positive number')
			except TypeError:
				raise ValidationError('Grade must be a (positive) number')
	
	grade_scale = fields.Integer(related='assessment_id.grade_scale', store=True)	
	penalty = fields.Float('Penalty (%)', compute='_penalty')
	cancel_penalty = fields.Boolean(string='Cancel Penalty', default=False)
	egrade = fields.Float(string='Effective Grade (%)', compute='_grade', store=True, group_operator='avg')
	formatted_grade = fields.Char(string='Assigned Grade', compute='_grade')
	formatted_egrade = fields.Char(string='Grade', compute='_grade')
	grade_range = fields.Char(string='Grade Range', compute='_grade', store=True)
	wgrade = fields.Float(string='Weighted Grade', compute='_grade', store=True)
	
	max_grade = fields.Float(related='assessment_id.max_grade')
	min_grade = fields.Float(related='assessment_id.min_grade')
	avg_grade = fields.Float(related='assessment_id.avg_grade')
	

	@api.depends('grade', 'mgrade', 'bonus', 'grade_scale', 'grade_weighting', 'percentage', 'points')
	@api.onchange('grade', 'mgrade')
	def _grade(self):
		for rec in self:
			if not rec.grade or rec.grade == '':
				rec.egrade = 0.0
				rec.formatted_grade = 'Not graded yet'
				rec.formatted_egrade = 'Not graded yet'
				rec.grade_range = 'Not graded yet'
				return
			try:
				if float(rec.grade) < 0 or (rec.mgrade and float(rec.mgrade) < 0):
					raise ValidationError('The grade must be a positive number')
			except TypeError:
					raise ValidationError('The grade must be a (positive) number')
			
			pgrade = fields.Float.round(float(rec.grade) / rec.grade_scale * 100, 2)
			if rec.mgrade:
				pmgrade = fields.Float.round(float(rec.mgrade) / rec.grade_scale * 100, 2)
				if rec.assessment_id.makeup_grade_policy == 'max':
					pgrade = max(pgrade, pmgrade)
					rec.formatted_grade = f'max({rec.grade}, {rec.mgrade}) / {rec.grade_scale}'
				elif rec.assessment_id.makeup_grade_policy == 'bounded_max':
					pgrade = max(pgrade, min(pmgrade, rec.assessment_id.makeup_grade_upper_bound))
					rec.formatted_grade = f'max({rec.grade}, min({rec.mgrade}, upper-bound={rec.assessment_id.makeup_grade_upper_bound})) / {rec.grade_scale}'
				elif rec.assessment_id.makeup_grade_policy == 'avg':
					pgrade = fields.Float.round((pgrade + pmgrade) / 2, 2)
					rec.formatted_grade = f'avg({rec.grade}, {rec.mgrade}) / {rec.grade_scale}'
				elif rec.assessment_id.makeup_grade_policy == 'last':
					rec.formatted_grade = f'last({rec.grade}, {rec.mgrade}) / {rec.grade_scale}'
					pgrade = pmgrade
			else:
				rec.formatted_grade = f'{rec.grade} / {rec.grade_scale}'
			
			rec.egrade = pgrade + rec.bonus - rec.penalty			
			formatted_egrade = str(fields.Float.round(rec.egrade / 100 * rec.grade_scale, 2)) + ' / ' + str(rec.grade_scale) + ' - ' + str(rec.egrade) + '%'
			if rec.grade_weighting == 'percentage':
				rec.wgrade = rec.egrade * rec.percentage / 100
			elif rec.grade_weighting == 'points':
				rec.wgrade = fields.Float.round(rec.egrade / 100 * rec.points, 2)
				formatted_egrade += ' - ' + str(rec.wgrade) + ' Pts.'
			rec.formatted_egrade = formatted_egrade
			if rec.egrade >= 90:
				rec.grade_range = '[90 - 100%+]'
			elif rec.egrade >= 80:
				rec.grade_range = '[80 - 90%['
			elif rec.egrade >= 70:
				rec.grade_range = '[70 - 80%['
			elif rec.egrade >= 60:
				rec.grade_range = '[60 - 70%['
			else:
				rec.grade_range = '[0 - 60%['
			

	def _penalty(self):
		for rec in self:
			if rec.cancel_penalty:
				rec.penalty = 0.0
			else:
				rec.penalty = 0.0

	