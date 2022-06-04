from odoo import models, fields


class Portfolio(models.Model):
	_name = 'a3quality.portfolio'
	_description = 'Portfolio'

	name = fields.Char('Name', required=True)
	section_id = fields.Many2one('a3roster.section', 'Section', required=True)
	