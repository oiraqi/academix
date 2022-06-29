from odoo import models, fields


class Resource(models.Model):
	_name = 'a3lms.resource'
	_description = 'Resource'

	name = fields.Char('Name', required=True)
	module_id = fields.Many2one(comodel_name='a3lms.module', string='Module', required=True)
	course_id = fields.Many2one(comodel_name='a3lms.course', string='LMS Course', required=True)
	file = fields.Binary(string='File')
	url = fields.Char(string='URL')	
	