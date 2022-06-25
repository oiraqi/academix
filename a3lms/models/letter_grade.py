from odoo import models, fields


class LetterGrade(models.Model):
	_name = 'a3lms.letter.grade'
	_description = 'LetterGrade'

	name = fields.Char('Name', required=True)
	min = fields.Float(string='Min Grade (Included)', required=True)
	max = fields.Float(string='Max Grade (Excluded)', required=True)
	passing = fields.Binary(string='Passing Grade', default=True, required=True)
	
	