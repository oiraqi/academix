from odoo import models, fields, api


class AssessmentLine(models.Model):
	_name = 'a3lms.assessment.line'
	_description = 'AssessmentLine'
	_order = 'student_id'

	name = fields.Char('Name', related='assessment_id.name')
	student_id = fields.Many2one(comodel_name='a3.student', string='Student', required=True)	
	assessment_id = fields.Many2one(comodel_name='a3lms.assessment', string='Assessment', required=True)
	program_id = fields.Many2one(comodel_name='a3catalog.program', related='student_id.program_id', store=True)	
	course_id = fields.Many2one(comodel_name='a3lms.course', related='assessment_id.course_id', store=True)
	section_id = fields.Many2one(comodel_name='a3roster.section', related='assessment_id.section_id', store=True)
	module_id = fields.Many2one(comodel_name='a3lms.module', related='assessment_id.module_id', store=True)
	technique_id = fields.Many2one(comodel_name='a3lms.weighted.technique', related='assessment_id.technique_id', store=True)
	grade_grouping = fields.Selection(related='assessment_id.course_id.grade_grouping', store=True)
	grade_weighting = fields.Selection(related='assessment_id.course_id.grade_weighting', store=True)
	points = fields.Integer(related='assessment_id.points', store=True)
	module_percentage = fields.Float(related='module_id.percentage', store=True)
	technique_percentage = fields.Float(related='technique_id.percentage', store=True)
	assessment_percentage = fields.Float(related='assessment_id.percentage', store=True)
	percentage = fields.Float(related='assessment_id.percentage', store=True)
	grade = fields.Float(string='Grade', default=0.0)
	bonus = fields.Float(related='assessment_id.bonus', store=True)
	penalty = fields.Float('Penalty', compute='_penalty')
	egrade = fields.Float(string='Grade', compute='_egrade', store=True)
	wgrade = fields.Float(string='Weighted Grade', compute='_wgrade', store=True)

	@api.depends('grade', 'bonus')
	@api.onchange('grade', 'bonus')
	def _egrade(self):
		for rec in self:
			rec.egrade = rec.grade + rec.bonus - rec.penalty

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

