from odoo import models, fields


class Publisher(models.Model):
	_name = 'ixresearch.publisher'
	_description = 'Publisher'

	name = fields.Char('Name', required=True)
	