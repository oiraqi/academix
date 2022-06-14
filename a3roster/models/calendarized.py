from odoo import models, fields


class Calendarized(models.Model):
	_inherit = 'a3.calendarized'

	def _make_reservation(self):
		self.ensure_one()
		self.env['a3roster.reservation'].create({
            'room_type': self.room_id.type,
            'room_capacity': '5',
            'purpose': 'presentation',
            'description': 'Project Defense',
            'room_id': self.room_id.id,
            'start_time': self.start_time,
            'end_time': self.end_time
        })
	
	