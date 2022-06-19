from odoo import models, fields


class OfficeHour(models.Model):
	_name = 'a3roster.office.hour'
	_description = 'Office Hour'
	_inherit = ['a3.faculty.owned', 'a3roster.scheduled']

	name = fields.Char(related='timeslot')
	