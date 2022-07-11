from odoo import models, fields


class Tag(models.Model):
	_name = 'ixdms.tag'
	_description = 'Tag'

	name = fields.Char('Name', required=True)
	