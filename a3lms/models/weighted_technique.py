from odoo import models, fields


class WeightedTechnique(models.Model):
	_name = 'a3lms.weighted.technique'
	_description = 'Weighted Technique'

	technique_id = fields.Many2one(comodel_name='a3lms.assessment.technique', string='Assessment Technique', required=True)
	name = fields.Char(related='technique_id.name')	
	weight = fields.Float(string='%', required=True, default=0.0)
	course_id = fields.Many2one(comodel_name='a3lms.course', string='LMS Course', required=True)
	