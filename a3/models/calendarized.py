from odoo import api, models, fields


class Calendarized(models.AbstractModel):
	_name = 'a3.calendarized'
	_description = 'Calendarized'

	event_id = fields.Many2one(comodel_name='calendar.event', string='Event')
	start_time = fields.Datetime('Start Time')
	end_time = fields.Datetime('End Time')
	building_id = fields.Many2one(comodel_name='a3.building', string='Building')
	room_id = fields.Many2one(comodel_name='a3.room', string='Room')
	videocall_location = fields.Char(string='Conference URL')
	

	@api.onchange('building_id')
	def _room(self):
		for rec in self:
			if rec.building_id and rec.building_id.room_ids:
				rec.room_id = rec.building_id.room_ids[0]
	
	

	def set_event(self, name, start, stop, location, videocall_location=False, partner_ids=False):
		for rec in self:
			if not rec.event_id:
				rec.event_id = self.env['calendar.event'].create({
					'name': name,
					'start': start,
					'stop': stop,
					'location': location,
					'videocall_location': videocall_location,
					'privacy': 'private',
					'allday': False,
					'partner_ids': partner_ids
				})
	