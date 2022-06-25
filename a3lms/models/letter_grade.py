from odoo import models, fields


class LetterGrade(models.Model):
	_name = 'a3lms.letter.grade'
	_description = 'LetterGrade'

	name = fields.Char('Name', required=True)
	