from odoo import models, fields


class Calendarized(models.AbstractModel):
	_name = 'a3.calendarized'
	_description = 'Calendarized'

	event_id = fields.Many2one(comodel_name='calendar.event', string='Event')
	event_start = fields.Datetime('Start Time')
	event_stop = fields.Datetime('End Time')

	def set_event(self, name, start, stop, partner_ids=False):
		for rec in self:
			if not rec.event_id:
				rec.event_id = self.env['calendar.event'].create({
					'name': name,
					'start': start,
					'stop': stop,
					'privacy': 'private',
					'allday': False,
					'partner_ids': partner_ids
				})
	