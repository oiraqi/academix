from odoo import models, fields


class Degree(models.Model):
	_name = 'ixcrm.degree'
	_description = 'Degree'

	name = fields.Char('Name', required=True)
	education_system_id = fields.Many2one(comodel_name='ixcrm.education.system', string='Education System', required=True)
	sequence = fields.Integer(string='Sequence')
	
	