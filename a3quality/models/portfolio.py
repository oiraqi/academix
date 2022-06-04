from odoo import models, fields


class Portfolio(models.Model):
	_name = 'a3quality.portfolio'
	_description = 'Portfolio'

	name = fields.Char('Name', required=True)
	