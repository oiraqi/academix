from odoo import models, fields


class Publisher(models.Model):
	_name = 'a3research.publisher'
	_description = 'Publisher'

	name = fields.Char('Name', required=True)
	