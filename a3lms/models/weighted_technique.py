from odoo import models, fields


class WeightedTechnique(models.Model):
	_name = 'a3lms.weighted.technique'
	_description = 'Weighted Technique'

	technique_id = fields.Many2one(comodel_name='a3lms.assessment.technique', string='Assessment Technique', required=True)
	name = fields.Char(related='technique_id.name')
	sequence = fields.Integer(string='Sequence', required=True)
	points = fields.Integer(string='Points', compute='_points')
	percentage = fields.Float(string='%', default=0.0)
	course_id = fields.Many2one(comodel_name='a3lms.course', string='LMS Course', required=True)
	assessment_ids = fields.One2many(comodel_name='a3lms.assessment', inverse_name='technique_id', string='Assessments')

	def _points(self):
		for rec in self:
			assessments = self.env['a3lms.assessment'].search([('course_id', '=', rec.course_id.id), ('technique_id', '=', rec.id)])
			if assessments:
				rec.points = sum([assessment.points for assessment in assessments])
			else:
				rec.points = 0
	