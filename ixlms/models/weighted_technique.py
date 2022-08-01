from odoo import models, fields, api


class WeightedTechnique(models.Model):
	_name = 'ixlms.weighted.technique'
	_description = 'Weighted Technique'
	_sql_constraints = [('course_technique_ukey', 'unique(course_id, technique_id)', 'Assessment techniques: Remove duplicates!')]

	technique_id = fields.Many2one(comodel_name='ixlms.assessment.technique', string='Assessment Technique', required=True)
	name = fields.Char(related='technique_id.name')
	sequence = fields.Integer(string='Sequence', required=True)
	points = fields.Integer(string='Points', compute='_points')
	percentage = fields.Float(string='%', compute='_percentage')
	course_id = fields.Many2one(comodel_name='ixlms.course', string='LMS Course', required=True)
	assessment_ids = fields.One2many(comodel_name='ixlms.assessment', inverse_name='technique_id', string='Assessments')	

	@api.onchange('assessment_ids')
	def _points(self):
		for rec in self:			
			if rec.assessment_ids:
				rec.points = sum([assessment.points for assessment in rec.assessment_ids])
			else:
				rec.points = 0

	@api.onchange('assessment_ids')
	def _percentage(self):
		for rec in self:			
			if rec.assessment_ids:
				rec.percentage = sum([assessment.percentage for assessment in rec.assessment_ids])
			else:
				rec.percentage = 0
	