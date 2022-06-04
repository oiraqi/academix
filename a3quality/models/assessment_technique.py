from odoo import models, fields


class AssessmentTechnique(models.Model):
	_name = 'a3quality.assessment.technique'
	_description = 'Assessment Technique'
	_order = 'name'

	name = fields.Char('Name', required=True)
	