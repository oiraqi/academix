from odoo import models, fields


class EducationSystem(models.Model):
	_name = 'ixcrm.education.system'
	_description = 'EducationSystem'

	name = fields.Char('Name', required=True)
	degree_ids = fields.One2many(comodel_name='ixcrm.degree', inverse_name='education_system_id', string='Degrees')
	