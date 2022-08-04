from odoo import models, fields


class Resource(models.Model):
	_name = 'ixlms.resource'
	_description = 'Resource'

	name = fields.Char('Name', required=True)	
	file = fields.Binary(string='File')
	url = fields.Char(string='URL')	
	course_id = fields.Many2one(comodel_name='ix.course', string='Course', required=True)
	
	
	