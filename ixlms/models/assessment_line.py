from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AssessmentLine(models.Model):
	_name = 'ixlms.assessment.line'
	_description = 'AssessmentLine'
	_inherit = 'ix.expandable'
	_order = 'egrade desc'

	name = fields.Char('Name', related='student_id.name', store=True)
	student_id = fields.Many2one(comodel_name='ix.student', string='Student', required=True)	
	assessment_id = fields.Many2one(comodel_name='ixlms.assessment', string='Assessment', required=True)
	program_id = fields.Many2one(comodel_name='ixcatalog.program', related='student_id.program_id', store=True)	
	course_id = fields.Many2one(comodel_name='ixlms.course', related='assessment_id.course_id', store=True)
	section_id = fields.Many2one(comodel_name='ixroster.section', related='assessment_id.section_id', store=True)
	module_id = fields.Many2one(comodel_name='ixlms.module', related='assessment_id.module_id', store=True)
	technique_id = fields.Many2one(comodel_name='ixlms.weighted.technique', related='assessment_id.technique_id', store=True)
	grade_grouping = fields.Selection(related='assessment_id.course_id.grade_grouping', store=True)
	grade_weighting = fields.Selection(related='assessment_id.course_id.grade_weighting', store=True)
	points = fields.Integer(related='assessment_id.points', store=True)
	module_percentage = fields.Float(related='module_id.percentage', store=True)
	technique_percentage = fields.Float(related='technique_id.percentage', store=True)
	assessment_percentage = fields.Float(related='assessment_id.percentage', store=True)
	percentage = fields.Float(related='assessment_id.percentage', store=True)	
	bonus = fields.Float(related='assessment_id.bonus', store=True)
	
	submission_type = fields.Selection(related='assessment_id.submission_type')
	teamwork = fields.Boolean(related='assessment_id.teamwork')
	submission_ids = fields.Many2many('ixlms.assessment.submission', 'ixlms_assessment_line_submission', 'assessment_line_id', 'submission_id', string='Submissions')
	grade = fields.Char(string='Assigned Grade', default='')

	@api.constrains('grade')
	def _check_grade(self):
		for rec in self:
			if rec.grade and float(rec.grade) < 0:
				raise ValidationError(f'Grade must be a positive number: {rec.grade}')
	
	grade_scale = fields.Integer(related='assessment_id.grade_scale', store=True)	
	penalty = fields.Float('Penalty', compute='_penalty')
	cancel_penalty = fields.Boolean(string='Cancel Penalty', default=False)
	egrade = fields.Float(string='Grade', compute='_egrade', store=True)
	grade_range = fields.Char(string='Grade Range', compute='_egrade', store=True)
	wgrade = fields.Float(string='Weighted Grade', compute='_wgrade', store=True)
	
	max_grade = fields.Float(related='assessment_id.max_grade')
	min_grade = fields.Float(related='assessment_id.min_grade')
	avg_grade = fields.Float(related='assessment_id.avg_grade')
	

	@api.depends('grade', 'bonus', 'cancel_penalty')
	@api.onchange('grade', 'bonus', 'cancel_penalty')
	def _egrade(self):
		for rec in self:
			if not rec.grade or rec.grade == '':
				rec.egrade = 0.0
				rec.grade_range = 'Not graded yet'
				return
			
			if float(rec.grade) < 0:
				raise ValidationError('The grade must be a positive number')
			
			rec.egrade = float(rec.grade) / rec.grade_scale * 100 + rec.bonus - rec.penalty
			if rec.egrade >= 90:
				rec.grade_range = '90%+'
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
				rec.penalty = 5.0

	@api.depends('egrade', 'grade_weighting', 'percentage', 'points')
	def _wgrade(self):
		for rec in self:
			if rec.grade_weighting == 'percentage':
				rec.wgrade = rec.egrade * rec.percentage / 100
			elif rec.grade_weighting == 'points':
				rec.wgrade = (rec.egrade / 100) * rec.points

