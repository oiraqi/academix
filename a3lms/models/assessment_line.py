from odoo import models, fields, api


class AssessmentLine(models.Model):
	_name = 'a3lms.assessment.line'
	_description = 'AssessmentLine'

	name = fields.Char('Name', related='assessment_id.name')
	assessment_id = fields.Many2one(comodel_name='a3lms.assessment', string='Assessment', required=True)
	module_id = fields.Many2one(comodel_name='a3lms.module', related='assessment_id.module_id', store=True)
	technique_id = fields.Many2one(comodel_name='a3lms.weighted.technique', related='assessment_id.technique_id', store=True)
	grade_grouping = fields.Selection(related='assessment_id.course_id.grade_grouping', store=True)
	grade_weighting = fields.Selection(related='assessment_id.course_id.grade_weighting', store=True)
	points = fields.Integer(related='assessment_id.points', store=True)
	module_percentage = fields.Float(related='module_id.percentage', store=True)
	technique_percentage = fields.Float(related='technique_id.percentage', store=True)
	assessment_percentage = fields.Float(related='assessment_id.percentage', store=True)
	percentage = fields.Float(string='Percentage', compute='_percentage', store=True)
	grade = fields.Float(string='Grade', default=0.0)
	bonus = fields.Float(related='assessment_id.bonus', store=True)
	bgrade = fields.Float(string='Grade', compute='_bgrade', store=True)
	wgrade = fields.Float(string='Weighted Grade', compute='_wgrade', store=True)

	@api.depends('grade', 'bonus')
	@api.onchange('grade', 'bonus')
	def _bgrade(self):
		for rec in self:
			rec.bgrade = rec.grade + rec.bonus

	@api.depends('grade_grouping', 'module_percentage', 'technique_percentage', 'assessment_percentage')
	def _percentage(self):
		for rec in self:
			if rec.grade_grouping == 'module':
				rec.percentage = rec.module_percentage * rec.assessment_percentage
			elif rec.grade_grouping == 'technique':
				rec.percentage = rec.technique_percentage * rec.assessment_percentage
			else:
				rec.percentage = 0

	@api.depends('bgrade', 'grade_weighting', 'percentage', 'points')
	def _wgrade(self):
		for rec in self:
			if rec.grade_weighting == 'percentage':
				rec.wgrade = rec.bgrade * rec.percentage
			elif rec.grade_weighting == 'points':
				rec.wgrade = (rec.bgrade / 100) * rec.points

