# -*- coding: utf-8 -*-
###############################################################################
#
#    Al Akhawayn University in Ifrane -- AUI
#    Copyright (C) 2022-TODAY AUI(<http://www.aui.ma>).
#
#    Author: Omar Iraqi Houssaini | https://github.com/oiraqi
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

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