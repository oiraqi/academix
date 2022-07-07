from odoo import models, fields, api
from odoo.exceptions import UserError


class LetterGrade(models.Model):
	_name = 'ixlms.letter.grade'
	_description = 'LetterGrade'
	_order = 'min desc'
	_sql_constraints = [('name_ukey', 'unique(name)', 'Name already exists')]

	name = fields.Char('Name', required=True)
	min = fields.Float(string='Min Grade (Included)', required=True)
	max = fields.Float(string='Max Grade (Excluded)', required=True)
	passing = fields.Boolean(string='Passing Grade', default=True, required=True)
	

	@api.model
	def evaluate(self, grade):
		letter_grade = self.search([('min', '<=', grade), ('max', '>', grade)])
		if letter_grade:
			return letter_grade.name, letter_grade.passing
		
		raise UserError('Strange grade!')