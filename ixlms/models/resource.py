from odoo import models, fields


class Resource(models.Model):
	_name = 'ixlms.resource'
	_description = 'Resource'

	name = fields.Char('Name', required=True)	
	content = fields.Html(string='Content', required=True)
	
	