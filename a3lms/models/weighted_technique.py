from odoo import models, fields


class WeightedTechnique(models.Model):
	_name = 'a3lms.weighted.technique'
	_description = 'Weighted Technique'

	technique_id = fields.Many2one(comodel_name='a3lms.assessment.technique', string='Assessment Technique', required=True)
	name = fields.Char(related='technique_id.name')	
	weight = fields.Float(string='Points', required=True, default=0.0)
	course_id = fields.Many2one(comodel_name='a3lms.course', string='LMS Course', required=True)
	total_assessment_weights = fields.Float(compute='_total_assessment_weights')

	def _total_assessment_weights(self):
		for rec in self:
			assessments = self.env['a3ls.assessment'].search([('course_id', '=', rec.course_id.id), ('technique_id', '=', rec.technique_id.id)])
			if assessments:
				rec.total_assessment_weights = sum([assessment.weight for assessment in assessments])
			else:
				rec.total_assessment_weights = 0
	