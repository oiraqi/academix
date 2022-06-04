from odoo import models, fields


class AssessmentTechnique(models.Model):
	_name = 'a3quality.assessment.technique'
	_description = 'AssessmentTechnique'

	name = fields.Char('Name', required=True)
	