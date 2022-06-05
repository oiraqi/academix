from odoo import models, fields


class AssessmentTechnique(models.Model):
	_name = 'a3quality.assessment.technique'
	_description = 'Assessment Technique'
	_order = 'sequence'

	name = fields.Char('Name', required=True)
	sequence = fields.Integer(string='Sequence', default=1, required=True)
	
	