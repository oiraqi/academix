from odoo import models, fields


class OfficeHour(models.Model):
	_name = 'ixroster.office.hour'
	_description = 'Office Hour'
	_inherit = ['ix.faculty.owned', 'ixroster.scheduled']

	name = fields.Char(related='timeslot')
	