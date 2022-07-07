from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AssessmentLine(models.Model):
	_name = 'ixlms.assessment.line'
	_description = 'AssessmentLine'
	_inherit = 'ix.expandable'
	_order = 'egrade desc'
	_sql_constraints = [('student_assessment_ukey', 'unique(student_id, assessment_id)', 'Assessment line already exists')]

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
			try:
				if rec.grade and float(rec.grade) < 0:
					raise ValidationError('Grade must be a positive number')
			except TypeError:
				raise ValidationError('Grade must be a (positive) number')
	
	grade_scale = fields.Integer(related='assessment_id.grade_scale')	
	penalty = fields.Float('Penalty (%)', compute='_penalty')
	cancel_penalty = fields.Boolean(string='Cancel Penalty', default=False)
	egrade = fields.Float(string='Effective Grade (%)', compute='_grade', store=True)
	formatted_grade = fields.Char(string='Assigned Grade', compute='_grade')
	formatted_egrade = fields.Char(string='Assigned Grade', compute='_grade')
	grade_range = fields.Char(string='Grade Range', compute='_grade', store=True)
	wgrade = fields.Float(string='Weighted Grade', compute='_grade', store=True)
	
	max_grade = fields.Float(related='assessment_id.max_grade')
	min_grade = fields.Float(related='assessment_id.min_grade')
	avg_grade = fields.Float(related='assessment_id.avg_grade')
	

	@api.depends('grade', 'bonus')
	@api.onchange('grade', 'bonus')
	def _grade(self):
		for rec in self:
			if not rec.grade or rec.grade == '':
				rec.egrade = 0.0
				rec.formatted_grade = 'Not graded yet'
				rec.formatted_egrade = 'Not graded yet'
				rec.grade_range = 'Not graded yet'
				return
			try:
				if float(rec.grade) < 0:
					raise ValidationError('The grade must be a positive number')
			except TypeError:
					raise ValidationError('The grade must be a (positive) number')
			
			pgrade = float(rec.grade) / rec.grade_scale * 100
			rec.egrade = pgrade + rec.bonus - rec.penalty
			rec.formatted_grade = f'{rec.grade} / {rec.grade_scale} ({pgrade}%)'
			formatted_egrade = str(rec.egrade / 100 * rec.grade_scale) + ' / ' + str(rec.grade_scale) + ' - ' + str(rec.egrade) + '%'
			if rec.grade_weighting == 'points':				
				formatted_egrade += ' - ' + str(rec.wgrade) + ' Pts.'				
			rec.formatted_egrade = formatted_egrade
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

	@api.depends('grade_weighting', 'percentage', 'points')
	@api.onchange('grade_weighting', 'percentage', 'points')
	def _grade(self):
		for rec in self:
			if not rec.grade or rec.grade == '':		
				return
			try:
				if float(rec.grade) < 0:
					raise ValidationError('The grade must be a positive number')
			except TypeError:
					raise ValidationError('The grade must be a (positive) number')
			
			pgrade = float(rec.grade) / rec.grade_scale * 100
			rec.egrade = pgrade + rec.bonus - rec.penalty

			if rec.grade_weighting == 'percentage':			
				rec.wgrade = rec.egrade * rec.percentage / 100
			elif rec.grade_weighting == 'points':
				rec.wgrade = rec.egrade / 100 * rec.points