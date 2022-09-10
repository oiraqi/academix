from odoo import models, fields


class EducationSystem(models.Model):
	_name = 'ixadmission.education.system'
	_description = 'EducationSystem'

	name = fields.Char('Name', required=True)
	degree_ids = fields.One2many(comodel_name='ixadmission.degree', inverse_name='education_system_id', string='Degrees')
	