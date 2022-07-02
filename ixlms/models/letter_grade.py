from odoo import models, fields


class LetterGrade(models.Model):
	_name = 'ixlms.letter.grade'
	_description = 'LetterGrade'
	_order = 'min desc'

	name = fields.Char('Name', required=True)
	min = fields.Float(string='Min Grade (Included)', required=True)
	max = fields.Float(string='Max Grade (Excluded)', required=True)
	passing = fields.Boolean(string='Passing Grade', default=True, required=True)
	
	