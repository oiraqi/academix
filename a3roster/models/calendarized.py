from odoo import models, fields


class Calendarized(models.AbstractModel):
	_inherit = 'a3.calendarized'

	def set_event(self, name, partner_ids=False, videocall_location=False):		
		super(Calendarized, self).set_event(name, partner_ids, videocall_location)
		self._make_reservation()

	def _make_reservation(self):
		for rec in self:
			self.env['a3roster.reservation'].create({
	            'room_type': rec.room_id.type,
    	        'room_capacity': '5',
        	    'purpose': 'presentation',
            	'description': 'Project Defense',
	            'room_id': rec.room_id.id,
    	        'start_time': rec.start_time,
        	    'end_time': rec.end_time,
				'event_id': rec.event_id.id,
        	})
	
	