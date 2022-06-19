from odoo import models


class OfficeHour(models.Model):
	_name = 'a3roster.office.hour'
	_description = 'Office Hour'
	_inherit = ['a3.faculty.owned', 'a3roster.scheduled']

	