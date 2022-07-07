from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class LetterGrade(models.Model):
	_name = 'ixlms.letter.grade'
	_description = 'LetterGrade'
	_order = 'min desc'
	_sql_constraints = [('name_ukey', 'unique(name)', 'Name already exists')]

	name = fields.Char('Name', required=True)
	min = fields.Float(string='Min Grade (Included)', required=True)
	max = fields.Float(string='Max Grade (Excluded)', required=True)
	passing = fields.Boolean(string='Passing Grade', default=True, required=True)

	@api.constrains('min', 'max')
	def _check_min_max(self):
		for rec in self:
			if rec.min < 0:
				raise ValidationError('Min must be positive')
			if rec.max <= 0:
				raise ValidationError('Max must be strictly positive')
			if rec.max <= rec.min:
				raise ValidationError('Min must be (strictly) smaller than Max')
	

	@api.model
	def evaluate(self, grade):
		letter_grade = self.search([('min', '<=', grade), ('max', '>', grade)])
		if letter_grade:
			return letter_grade.name, letter_grade.passing
		
		raise UserError('Strange grade!')