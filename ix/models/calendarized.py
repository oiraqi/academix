from odoo import api, models, fields


class Calendarized(models.AbstractModel):
	_name = 'ix.calendarized'
	_description = 'Calendarized'

	event_id = fields.Many2one(comodel_name='calendar.event', string='Event')
	start_time = fields.Datetime('Start Time')
	end_time = fields.Datetime('End Time')
	building_id = fields.Many2one(comodel_name='ix.building', string='Building')
	room_id = fields.Many2one(comodel_name='ix.room', string='Location')
	videocall_location = fields.Char(string='Conference URL')
	term_id = fields.Many2one('ix.term', string='Term')
	

	@api.onchange('building_id')
	def _room(self):
		for rec in self:
			if rec.building_id and rec.building_id.room_ids:
				rec.room_id = rec.building_id.room_ids[0]
	

	def set_event(self, name, partner_ids=[], videocall_location=''):
		for rec in self:
			if not rec.event_id:
				rec.event_id = self.env['calendar.event'].create({
					'name': name,
					'start': rec.start_time,
					'stop': rec.end_time,
					'location': rec.room_id.name,
					'videocall_location': videocall_location,
					'privacy': 'private',
					'allday': False,
					'partner_ids': [(6, 0, partner_ids)],
					'term_id': rec.term_id.id,
				})

	@api.depends('room_id', 'start_time', 'end_time')
	def update_calendar(self):
		for rec in self:
			if rec.event_id:
				if rec.event_id.start != rec.start_time:
					rec.event_id.start = rec.start_time
				if rec.event_id.stop != rec.end_time:
					rec.event_id.stop = rec.end_time
				if rec.event_id.location != rec.room_id.name:
					rec.event_id.location = rec.room_id.name

	