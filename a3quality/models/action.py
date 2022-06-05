from odoo import models, fields


class Action(models.Model):
	_name = 'a3quality.action'
	_description = 'Action'

	name = fields.Char('Name', required=True)
	