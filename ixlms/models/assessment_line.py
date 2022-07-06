from odoo import models, fields, api


class AssessmentLine(models.Model):
	_name = 'ixlms.assessment.line'
	_description = 'AssessmentLine'
	_inherit = 'ix.expandable'
	_order = 'student_id'

	name = fields.Char('Name', compute='_set_name', store=True)

	@api.depends('assessment_id', 'student_id')
	@api.onchange('assessment_id', 'student_id')
	def _set_name(self):
		for rec in self:
			if rec.assessment_id and rec.student_id:
				rec.name = rec.assessment_id.name + ' / ' + rec.student_id.name
	
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
	submission_ids = fields.Many2many('ixlms.assessment.submission', 'ixlms_assessment_line_submission', 'assessment_line_id', 'submission_id', string='Submissions')
	grade = fields.Float(string='Grade', default=0.0)
	penalty = fields.Float('Penalty', compute='_penalty')
	cancel_penalty = fields.Boolean(string='Cancel Penalty', default=False)	
	egrade = fields.Float(string='Grade', compute='_egrade', store=True)
	wgrade = fields.Float(string='Weighted Grade', compute='_wgrade', store=True)
	
	max_grade = fields.Float(related='assessment_id.max_grade')
	min_grade = fields.Float(related='assessment_id.min_grade')
	avg_grade = fields.Float(related='assessment_id.avg_grade')
	

	@api.depends('grade', 'bonus', 'cancel_penalty')
	@api.onchange('grade', 'bonus', 'cancel_penalty')
	def _egrade(self):
		for rec in self:
			rec.egrade = rec.grade + rec.bonus - (rec.cancel_penalty and 0 or rec.penalty)

	def _penalty(self):
		for rec in self:
			rec.penalty = 0.0

	@api.depends('egrade', 'grade_weighting', 'percentage', 'points')
	def _wgrade(self):
		for rec in self:
			if rec.grade_weighting == 'percentage':
				rec.wgrade = rec.egrade * rec.percentage
			elif rec.grade_weighting == 'points':
				rec.wgrade = (rec.egrade / 100) * rec.points

