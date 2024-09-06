from odoo import models, fields, api


class OfficeHour(models.Model):
	_name = 'ixroster.office.hour'
	_description = 'Office Hour'
	_inherit = ['ix.faculty.owned', 'ixroster.scheduled']
	_mapping = {'f2f': 'Face To Face', 'online': 'Online'}

	def _compute_name(self):
		for rec in self:
			rec.name = rec.timeslot + ' (' + OfficeHour._mapping[rec.type] + ')'
	
	name = fields.Char(compute='_compute_name')
	type = fields.Selection(string='Type', selection=[('f2f', 'Face To Face'), ('online', 'Online')], default='f2f')
	